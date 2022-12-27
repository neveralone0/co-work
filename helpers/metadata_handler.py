from rest_framework.metadata import BaseMetadata


class MinimalMetadata(BaseMetadata):
    """
    Don't include field and other information for `OPTIONS` requests.
    Just return the name, description and allowed methods.
    """
    def determine_metadata(self, request, view):
        return {
            'name': view.get_view_name(),
            'description': view.get_view_description(),
            'allowed_request_methods': [i for i in view.allowed_methods],
            # 'allowed_request_methods': view._allowed_methods(),
        }
