const shopContent = document.getElementById("shopContent");
const cart = []; //Este es nuyestro carrito, un array vacio

productos.forEach((product)=>{
    const content = document.createElement("div");
    content.innerHTML = `
    <img src="${product.img}">
    <h3>${product.productName}</h3>
    <p>${product.price} $</p>
  `;
      shopContent.append(content);
    const buyButton = document.createElement("button");
    buyButton.innerText = "Buy";

    content.append(buyButton);

   buyButton.addEventListener("click", ()=>{
      const repeat = cart.some((repeatProduct)=> repeatProduct.id === product -id);

      if(repeat){
        //Si el producto ya esta en la lista de compras lo quitamos
        cart.map((prod)=>{
          if (prod.id === product- id) {
            prod.quanty++;
            displayCartCounter();//SE AGREGO ESTO
          }
        });
      }else {
        cart.push({
            id: product.id,
            productName: product.productName,
            price: product.price,
            quanty: product.quanty,
            img: product.img,
        });  
        displayCartCounter() ;//Y ESTO
      }
    });
});
