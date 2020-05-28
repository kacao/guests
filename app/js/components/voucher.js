
class VoucherList extends HTMLElement {

  constructor() {
    super();

    var shadow = this.attachShadow({mode: 'open'});
    var ul = document.createElement('ul'); 
    var styles = document.createElement('link');
    styles.setAttribute('rel', 'stylesheet');
    styles.setAttribute('href', 'css/voucher.css');
    
    shadow.appendChild(styles); 
    shadow.appendChild(ul); 
  }

  _add_voucher(data) {
    var root = this.shadowRoot;
    let element = document.createElement('li');
    element.textContent += `<li><span>${data['code']}</span></li>`;
    root.appendChild(element);
  }

  _clear() {
    var root = this.shadowRoot;
    root.querySelector('ul').innerHTML = '';
  }

  update_list(data) {
    this._clear();
    for (const create_time in data) {
      let voucher = data[create_time];
      this._add_voucher(voucher);
    }
  }
}

/*class Voucher extends HTMLElement {

  constructor(data) {
    super();
    this._id = data['_id'];
    this.site_id = data['site_id'];
    this.create_time = data['create_time'];
    this.code = data['code'];
    this.admin_name = data['admin_name'];
    this.quota = data['quota'];
    this.duration = data['duration'];
    this.used = data['used'];
    this.status = data['status'];
    this.status_expires = data['status_expires'];

    var shadow = this.attachShadow({mode: 'open'});
    var li = document.createElement('li');
    var code = document.createElement('span');
    code.setAttribute('class', 'code');
    code.textContent = this.code;

    li.appendChild(code);
    //shadow.appendChild(styles);
    shadow.appendChild(li);
  }

}
*/

customElements.define('voucher-list', VoucherList);

