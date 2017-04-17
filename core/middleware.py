from django.contrib.auth.models import User

class GetActiveUser:
    def process_template_response(self, request, response):
        ctx = {}
        current_user = request.session.get('user', None)
        ctx['current_user'] = current_user if current_user else {'username': 'Anonimous'}
        ctx['user_list'] = User.objects.all().values('pk', 'username')
        if getattr(response, 'context_data', None):
            response.context_data.update(ctx)
        return response
