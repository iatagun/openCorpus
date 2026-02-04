"""
Custom security middleware
"""

from django.utils.deprecation import MiddlewareMixin
from accounts.models import AuditLog
import logging

logger = logging.getLogger('security')


class AuditLogMiddleware(MiddlewareMixin):
    """
    Middleware to automatically log user actions
    """
    
    def process_request(self, request):
        """Store request start time"""
        import time
        request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        """Log the request if user is authenticated"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Determine action type based on HTTP method
            method_action_map = {
                'GET': AuditLog.ActionType.VIEW,
                'POST': AuditLog.ActionType.CREATE,
                'PUT': AuditLog.ActionType.UPDATE,
                'PATCH': AuditLog.ActionType.UPDATE,
                'DELETE': AuditLog.ActionType.DELETE,
            }
            
            action = method_action_map.get(request.method, AuditLog.ActionType.VIEW)
            
            # Skip logging for certain paths
            skip_paths = ['/static/', '/media/', '/admin/jsi18n/']
            if not any(request.path.startswith(path) for path in skip_paths):
                try:
                    AuditLog.objects.create(
                        user=request.user,
                        action=action,
                        resource_type='HTTP_REQUEST',
                        description=f"{request.method} {request.path}",
                        ip_address=self.get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
                        extra_data={
                            'method': request.method,
                            'path': request.path,
                            'status_code': response.status_code,
                        }
                    )
                except Exception as e:
                    logger.error(f"Failed to create audit log: {e}")
        
        return response
    
    @staticmethod
    def get_client_ip(request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add additional security headers
    """
    
    def process_response(self, request, response):
        """Add custom security headers"""
        # Content Security Policy
        response['Content-Security-Policy'] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
        )
        
        # Additional headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response
