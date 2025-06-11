
//xử lý sự kiện khi ấn vào nút "+" hoặc "-" ở giỏ hàng
var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

	var url = '/update_item/'

	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then(response => {
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		return response.json();
	})
	.then(data => {
    console.log('Response data:', data);
		if(data.status === 'success'){
			// Bạn có thể reload trang hoặc cập nhật UI động tại đây
			location.reload();
		} else {
			alert('Cập nhật giỏ hàng thất bại!');
		}
	})
	.catch(error => {
		console.error('Lỗi:', error);
		alert('Lỗi khi cập nhật giỏ hàng!');
	});
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	updateCartCount();
}
function updateCartCount() {
	let cartItems = 0;
	for (let key in cart) {
		cartItems += cart[key].quantity;
	}
	let cartCountSpan = document.querySelector('.cart-count');
	if (cartCountSpan) {
		cartCountSpan.innerText = `Giỏ hàng (${cartItems})`;
	}
}