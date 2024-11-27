function createCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    const nameEQ = name + "=";
    const ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function showCookiePopup() {
    document.getElementById('cookie-popup').style.display = 'block';
}

document.getElementById('accept-cookies').onclick = function() {
    createCookie('cookiesAccepted', 'true', 30); // 30 días 
    document.getElementById('cookie-popup').style.display = 'none';
    location.reload();
};

document.getElementById('deny-cookies').onclick = function() {
    createCookie('cookiesAccepted', 'false', 30); // 30 días
    document.getElementById('cookie-popup').style.display = 'none';
};


window.onload = function() {
    if (!getCookie('cookiesAccepted')) {
        showCookiePopup();
    }
};