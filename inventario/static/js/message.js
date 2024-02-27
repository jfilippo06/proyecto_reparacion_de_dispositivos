document.getElementById('logout-link').addEventListener('click', function (e) {
    e.preventDefault();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Quieres cerrar la sesión?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/logout';
        }
    })
});

document.getElementById('cancelar_compra').addEventListener('click', function (e) {
    e.preventDefault();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Quieres cancelar la compra?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, cancelar compra',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/venta/cancelar_compra';
        }
    })
});

document.getElementById('facturar').addEventListener('click', function (e) {
    e.preventDefault();
    Swal.fire({
        title: '¿Estás seguro?',
        text: "¿Quieres realizar la compra?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Sí, realizar compra',
        cancelButtonText: 'No, cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            window.location.href = '/venta/facturar';
        }
    })
});