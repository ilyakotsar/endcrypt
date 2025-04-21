document.querySelectorAll('.btn-toggle-password').forEach(btn => {
    btn.addEventListener('click', function() {
        let password = document.getElementById('password');
        let icon;
        if (password.type === 'password') {
            password.type = 'text';
            icon = 'visibility-icon';
        } else {
            password.type = 'password';
            icon = 'visibility-off-icon';
        }
        btn.innerHTML = document.getElementById(icon).innerHTML;
    });
});

document.querySelectorAll('.btn-main').forEach(btn => {
    btn.addEventListener('click', function() {
        loader = btn.querySelector('.loader');
        loader.classList.remove('hidden');
    });
});

document.querySelectorAll('[copy]').forEach(btn => {
    btn.addEventListener('click', function() {
        let text = document.getElementById(btn.getAttribute('copy')).innerText;
        navigator.clipboard.writeText(text).then(() => {
            let btnText = btn.innerText;
            btn.innerText = 'Copied';
            setTimeout(() => {
                btn.innerText = btnText;
            }, 1000);            
        });
    });
});