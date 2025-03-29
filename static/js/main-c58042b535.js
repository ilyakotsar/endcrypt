document.querySelectorAll('.btn-toggle-password').forEach(btn => {
    btn.addEventListener('click', function() {
        let img = btn.querySelector('img');
        let password = document.getElementById('password');
        if (password.type === 'password') {
            password.type = 'text';
            img.src = '/static/img/visibility.svg';
        } else {
            password.type = 'password';
            img.src = '/static/img/visibility_off.svg';
        }
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