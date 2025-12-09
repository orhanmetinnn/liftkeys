# utils.py
def add_to_cart(request, product_id, answers=None):
    cart = request.session.get("cart", [])
    cart.append({
        "product_id": product_id,
        "answers": answers or {},  # soru_id: cevap şeklinde dict
    })
    request.session["cart"] = cart
    request.session.modified = True
