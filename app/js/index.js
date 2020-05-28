let w = window.location;
const API_URL = `${w.protocol}//${w.host}`;
const EP_VOUCHERS = `${API_URL}/api/vouchers`;

// populate a voucher-list element with vouchers
async function list_vouchers(list_ele) {
  res = await fetch(EP_VOUCHERS);
  if (res.ok) {
    let json = await res.json();
    list_ele.update_list(json['data']);
  } else {
    alert('fk');
  }
}

async function main() {
  list_ele = document.getElementById('voucher-list');
  await list_vouchers(list_ele);
}

main();


