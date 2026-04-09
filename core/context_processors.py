from products.models import Product, ProductVariant
from workshops.models import Booking, Workshop
from inquiries.models import QuoteRequest, ContactSubmission

def admin_dashboard(request):
    """Inject analytics stats into the Django admin index."""
    if request.path == '/admin/':
        # Simple counts for now
        total_products = Product.objects.count()
        total_bookings = Booking.objects.count()
        total_quotes = QuoteRequest.objects.count()
        converted_quotes = QuoteRequest.objects.filter(status='CONVERTED').count()
        
        conversion_rate = 0
        if total_quotes > 0:
            conversion_rate = round((converted_quotes / total_quotes) * 100, 2)

        stats = {
            'total_products': total_products,
            'total_bookings': total_bookings,
            'total_quotes': total_quotes,
            'converted_quotes': converted_quotes,
            'conversion_rate': conversion_rate,
        }
        return {'dashboard_stats': stats}
    return {}
