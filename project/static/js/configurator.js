function shop_configurator(opts) {
"use strict";

const {baseUrl, token} = opts
const fetchOpts = { headers: new Headers({'Authorization' : `Bearer ${token}`})}

class Section {
    categoryId = undefined
    //categoryBlockId = undefined
    //productsBlockId = undefined
    categoryNode = undefined
    productsNode = undefined

    constructor(categoryId){
        this.categoryId = categoryId
        //this.categoryBlockId = `#filters-${this.categoryId}`
        //this.productsBlockId = `#product-block-${this.categoryId}`
        this.categoryNode = document.querySelector(`#filters-${this.categoryId}`)
        this.productsNode = document.querySelector(`#product-block-${this.categoryId}`)

        this.categoryNode
            .querySelectorAll('button.filter')
            .forEach(btn =>  btn.addEventListener('click', () => this.renderProducts()))
    }

    renderProducts(){
        const manufFilter = this.categoryNode.querySelector('.filter-manufacturer')
        let query = `cat=${this.categoryId}`
        query+=`&man=${manufFilter.value}`
        console.log(query)

        this.productsNode.innerHTML = ''
        fetch(`${baseUrl}/products?${query}`, fetchOpts)
            .then(response => response.json())
            .then((data) => {
                data.forEach(product =>{
                    const prodRend = new ProductRenderer(product)
                    this.productsNode.appendChild(prodRend.render())
                })
            });
    }
}

let procs = new Section(1)
procs.renderProducts()
let ozu = new Section(2)
ozu.renderProducts()


function addFilterButtonListener(btn){
    let cat = btn.getAttribute('data-category')
    btn.addEventListener('click', () => {
        fetch(`${baseUrl}/users/current`, fetchOpts)
          .then(response => response.json())
          .then((data) => {
            console.log(data, cat);
          });
    })
}

function addOrderButtonListener(btn){
    let cat = btn.getAttribute('data-category')
    btn.addEventListener('click', () => {
        fetch(`${baseUrl}/users/current`, fetchOpts)
          .then(response => response.json())
          .then((data) => {
            console.log(data, cat);
          });
    })
}

//const filterButtons = document.querySelectorAll('button.filter')
//filterButtons.forEach(fb => addFilterButtonListener(fb))

const addToCartButtons = document.querySelectorAll('button.filter')
//addToCartButtons.

}