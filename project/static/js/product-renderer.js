class ProductRenderer{

    constructor(product){
        this.product = product
    }

    render(){
        const midCol = this.renderMidCol()
        midCol.appendChild(this.renderTitle())

        const chars = this.renderChars()
        chars.appendChild(this.renderVendorCode())

        const charsDetails = this.renderCharsDetails()
        charsDetails.appendChild(this.renderManufacturer())

        this.product.products_attributes.forEach(attr=>{
            charsDetails.appendChild(this.renderAttribute(attr))
        })

        chars.appendChild(charsDetails)
        midCol.appendChild(chars)

        const innerWrapper = this.renderInnerWrapper()
        innerWrapper.appendChild(this.renderPhoto())
        innerWrapper.appendChild(midCol)
        innerWrapper.appendChild(this.renderPrice())
        innerWrapper.appendChild(this.renderAddToCartButton())

        const outerWrapper = this.renderOuterWrapper()
        outerWrapper.appendChild(innerWrapper)
        return outerWrapper
    }

    renderOuterWrapper(){
        const li = document.createElement('li')
        li.className = "b-item"
        li.dataset.id_product = this.product.ProductId
        li.dataset.price = this.product.Price
        return li
    }

    renderInnerWrapper(product){
        const div = document.createElement('div')
        div.className = "b-cng-item-prod product_wrapper"
        div.dataset.id_product = this.product.ProductId
        return div
    }

    renderMidCol(){
        const div = document.createElement('div')
        div.className = "b-cngip-mid-col"
        return div
    }

    renderTitle(){
        const div = document.createElement('div')
        div.className = "b-cngip-head"
        div.innerHTML = `${this.product.Title}`
        return div;
    }

    renderPhoto(){
        const div = document.createElement('div')
        div.className = "b-cngip-pic"
        const photo = this.product.photos[0]
        div.innerHTML = `<img src="static/photos/${this.product.ProductId}/${photo.FileName}" width="100" height="100"/>`
        return div;
    }

    renderChars(){
     const div = document.createElement('div')
        div.className = "b-cngip-mc-meta"
        return div;
    }

    renderCharsDetails(){
        const div = document.createElement('div')
        div.className = "b-cngip-short-chars"
        return div;
    }

    renderVendorCode(){
        const div = document.createElement('div')
        div.className = "b-i-product-articul"
        div.innerHTML = `Артикул: <i>${this.product.ProductId}</i>`
        return div;
    }

    renderManufacturer(){
        const p = document.createElement('p')
        p.innerHTML = `Виробник: <a href="http://#" target="_blank">${this.product.Manufacturer.CompanyName}</a><br>`
        return p
    }

    renderAttribute(productAttr){
        const p = document.createElement('p')
        p.innerHTML = `${productAttr.Attribute.AttributeTitle}: ${productAttr.AttributeValue}<br>`
        return p
    }

    renderPrice(){
        const div = document.createElement('div')
        div.className = "b-cngip-meta-col"
        div.innerHTML = `<div class="b-cngip-price">${this.product.Price}<i>грн</i></div>`
        return div
    }

    renderAddToCartButton(){
        const div = document.createElement('div')
        div.className = "b-cngip-meta-btn"
        div.innerHTML = '<ul class="b-htconf-btns-list">'
            +'    <li>'
            +'       <a class="b-cngip-btn-add add_assembly_product"'
            +'           href="javascript: AlertMsg();">Додати</a>'
            +'    </li>'
            +'</ul>'
        return div
    }
}