// static/js/script.js
function fetchProducts() {
    fetch('/api/products/')
        .then(response => response.json())
        .then(data => {
            console.log('Danh sách sản phẩm:', data);
            const container = document.getElementById('product-container');
            container.innerHTML = ''; // Xóa nội dung cũ
            data.forEach(product => {
                const div = document.createElement('div');
                div.textContent = `Tên: ${product.product_name}, Giá: ${product.price}, Tồn kho: ${product.stock}`;
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Lỗi khi lấy sản phẩm:', error));
}

function fetchOrders() {
    fetch('/api/orders/')
        .then(response => response.json())
        .then(data => {
            console.log('Danh sách đơn hàng:', data);
            const container = document.getElementById('order-container');
            container.innerHTML = ''; // Xóa nội dung cũ
            data.forEach(order => {
                const div = document.createElement('div');
                div.textContent = `Đơn hàng ID: ${order.id}, Tổng giá: ${order.get_cart_total}, Trạng thái: ${order.complete}`;
                container.appendChild(div);
            });
        })
        .catch(error => console.error('Lỗi khi lấy đơn hàng:', error));
}

// Gọi API mỗi 5 giây
setInterval(fetchProducts, 5000);
setInterval(fetchOrders, 5000);

// Gọi ngay lần đầu khi tải trang
fetchProducts();
fetchOrders();