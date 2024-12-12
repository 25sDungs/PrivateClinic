// Sử dụng alert có sẵn
// function xacNhanQuyDinh() {
//     var result = confirm("Xác nhận thay đổi quy định?");
//     if (result) {
//         alert("Xác Nhận Thay Đổi!");
//     } else {
//         alert("Đã Hủy Thay Đổi!");
//     }
// }


// Tự tạo dialog
const dialog = document.querySelector("dialog");
const showButtons = document.querySelectorAll(".btnQuyDinh");
const closeButton = document.querySelector("dialog button");

// "Show the dialog" button opens the dialog modally
showButtons.forEach((showButton, index) => {
    //index: 0 là số bệnh nhân khám; 1 là tiền khám
    showButton.addEventListener("click", () => {
        dialog.showModal();
    })
});

// "Close" button closes the dialog
closeButton.addEventListener("click", () => {
    dialog.close();
});

function xacNhanQuyDinh() {
    //Ghi dữ liệu mới vào DB

}

var triggerTabList = [].slice.call(document.querySelectorAll('#myTab a'))
triggerTabList.forEach(function (triggerEl) {
  var tabTrigger = new bootstrap.Tab(triggerEl)

  triggerEl.addEventListener('click', function (event) {
    event.preventDefault()
    tabTrigger.show()
  })
})
var triggerEl = document.querySelector('#myTab a[href="#profile"]')
bootstrap.Tab.getInstance(triggerEl).show() // Select tab by name

var triggerFirstTabEl = document.querySelector('#myTab li:first-child a')
bootstrap.Tab.getInstance(triggerFirstTabEl).show() // Select first tab
