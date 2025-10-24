// =========================================================================
// BOOTSTRAP INITIALIZATION & MOBILE MENU LOGIC (Replaces Tailwind menu toggle)
// =========================================================================

// =========================================================================
// SCAN PAGE LOGIC (Webcam/Upload Toggle)
// =========================================================================

document.addEventListener('DOMContentLoaded', function() {
    const webcamRadio = document.getElementById("methodWebcam");
    const uploadRadio = document.getElementById("methodUpload");

    // Get the actual tab links that Bootstrap uses to switch content
    const webcamTabLink = document.querySelector('a[data-bs-target="#webcam-section"]');
    const uploadTabLink = document.querySelector('a[data-bs-target="#upload-section"]');

    // Function to handle the tab switch
    function switchTab(targetLink) {
        if (targetLink) {
            const tab = new bootstrap.Tab(targetLink);
            tab.show();
        }
    }

    // 1. Ensure clicking the radio button switches the tab content
    webcamRadio.addEventListener("change", () => {
        if (webcamRadio.checked) {
            switchTab(webcamTabLink);
        }
    });

    uploadRadio.addEventListener("change", () => {
        if (uploadRadio.checked) {
            switchTab(uploadTabLink);
        }
    });

    // 2. Ensure clicking the tab link updates the radio button state
    // This handles cases where a user might click the padding/area around the text,
    // which may only trigger the <a> link and not the <label>/radio button.
    webcamTabLink.addEventListener('shown.bs.tab', function (e) {
        webcamRadio.checked = true;
    });

    uploadTabLink.addEventListener('shown.bs.tab', function (e) {
        uploadRadio.checked = true;
    });


    // =========================================================================
    // Dummy buttons for Scan Result actions (Existing logic)
    // =========================================================================

    const copyBtn = document.getElementById("copyBtn");
    const openLinkBtn = document.getElementById("openLinkBtn");
    const scanResultText = document.getElementById("scanResultText");

    if (copyBtn && scanResultText) {
        copyBtn.onclick = () => {
            const text = scanResultText.innerText;
            if (text && text !== "No result yet") {
                navigator.clipboard.writeText(text);
                alert("Copied to Clipboard!");
            } else {
                alert("No content to copy.");
            }
        };
    }

    if (openLinkBtn && scanResultText) {
        openLinkBtn.onclick = () => {
            const text = scanResultText.innerText.trim();
            if (text.startsWith('http')) {
                 window.open(text, '_blank');
            } else {
                alert("The scanned result is not a valid link.");
            }
        };
    }
});


// =========================================================================
// GENERATE PAGE LOGIC (If using AJAX for generation/scanning)
// =========================================================================

// NOTE: Your original AJAX functions are provided below, assuming you still use 
// them instead of standard form submissions. If you switched to standard form 
// submissions in your Jinja templates, you may no longer need these functions.

/*
async function generateBarcode() {
    const text = document.getElementById("inputData").value;
    const type = document.getElementById("barcodeType").value;

    // Use a specific path if available, e.g., the URL from your form action
    const res = await fetch("/generate", { 
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ data: text, barcode_type: type }) // Adjusted keys to match template
    });

    const data = await res.json();

    const img = document.getElementById("outputImage");
    img.src = data.image ? ("data:image/png;base64," + data.image) : "https://placehold.co/400x400";
}


async function scanBarcode() {
    const file = document.getElementById("uploadInput").files[0];
    if (!file) return alert("Please upload an image.");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("/scan", { 
        method: "POST",
        body: formData
    });

    const data = await res.json();

    const resultTextElement = document.getElementById("scanResultText");
    if (resultTextElement) {
        resultTextElement.innerHTML = `
            Type: ${data.BarcodeType || 'N/A'}<br>
            Value: ${data.ValueDecoded || 'N/A'}
        `;
    }
}
*/



// =========================================================================
// THEME TOGGLE LOGIC
// =========================================================================

// Function to set a cookie
function setCookie(name, value, days) {
    let expires = "";
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/; SameSite=Lax";
}

// Function to get system preference
const getPreferredTheme = () => {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
};

// Function to manage theme setting
const setTheme = theme => {
    const htmlElement = document.documentElement;
    const bodyElement = document.body;
    let actualTheme = theme;

    if (theme === 'auto') {
        actualTheme = getPreferredTheme();
    }

    // 1. Apply theme to HTML attribute (Bootstrap's switch)
    htmlElement.setAttribute('data-bs-theme', actualTheme);

    // 2. Update the cookie for server-side persistence
    // We store the user's explicit choice ('light', 'dark', 'auto')
    setCookie('theme', theme, 30);

    // 3. Update the displayed icon in the dropdown and mobile button
    const iconMap = {
        'light': 'light_mode',
        'dark': 'dark_mode',
        'auto': 'contrast'
    };

    const iconElements = document.querySelectorAll('.theme-icon-active');
    iconElements.forEach(icon => {
        icon.textContent = iconMap[theme] || iconMap['auto'];
    });
};

// Function for mobile toggle (switches between light <-> dark <-> auto cycle)
const toggleTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 'auto';
    const currentChoice = document.cookie.split('; ').find(row => row.startsWith('theme='))?.split('=')[1] || 'auto';

    let newChoice;

    if (currentChoice === 'light') {
        newChoice = 'dark';
    } else if (currentChoice === 'dark') {
        newChoice = 'auto';
    } else { // 'auto' or not set
        newChoice = 'light';
    }

    setTheme(newChoice);
};

// Initialization on load: Binds dropdown clicks and sets initial theme
document.addEventListener('DOMContentLoaded', function() {
    // Determine the initial theme from the cookie set by the server
    const initialThemeChoice = document.cookie.split('; ').find(row => row.startsWith('theme='))?.split('=')[1] || 'auto';

    // Set the theme based on the choice/cookie
    setTheme(initialThemeChoice);

    // Add event listeners for the dropdown buttons
    document.querySelectorAll('[data-bs-theme-value]').forEach(toggle => {
        toggle.addEventListener('click', () => {
            const theme = toggle.getAttribute('data-bs-theme-value');
            setTheme(theme);
        });
    });

    // ... (rest of your existing DOMContentLoaded logic below) ...

    // (Existing mobile menu logic here)
    // ...
    // (Existing scan page logic here)
    // ...
});