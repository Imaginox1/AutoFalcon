// renderer.js
const gmailEntry = document.getElementById('gmail-entry');
const passwordEntry = document.getElementById('password-entry');
const toggleBtn = document.getElementById('toggle-password');
const nextBtn = document.getElementById('next-button');
const cancelBtn = document.getElementById('cancel-button');
const statusLabel = document.getElementById('status-label');

toggleBtn.addEventListener('click', () => {
  if (passwordEntry.type === 'password') {
    passwordEntry.type = 'text';
    toggleBtn.textContent = 'Hide Password';
  } else {
    passwordEntry.type = 'password';
    toggleBtn.textContent = 'Show Password';
  }
});

cancelBtn.addEventListener('click', () => {
  window.close();
});

// Next button binding
nextBtn.addEventListener('click', () => {
  performLogin();
});

// Enter key binding
document.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    performLogin();
  }
});

async function performLogin() {
  const gmailLocal = gmailEntry.value.trim();
  const pwd = passwordEntry.value;

  if (!gmailLocal || !pwd) {
    statusLabel.textContent = 'Please enter username and password.';
    statusLabel.style.color = 'red';
    return;
  }
  
  nextBtn.disabled = true;
  statusLabel.textContent = 'Processing...';
  statusLabel.style.color = 'black';

  try {
    // Call main process via preload bridge
    const result = await window.electronAPI.performLogin(gmailLocal, pwd);
    if (result && result.success) {
      statusLabel.textContent = result.message || 'Login Successful!';
      statusLabel.style.color = 'green';
    } else {
      statusLabel.textContent = result.message || 'Login Failed. Please check your email and password.';
      statusLabel.style.color = 'red';
    }
  } catch (err) {
    statusLabel.textContent = 'Login Failed. Please check your email and password.';
    statusLabel.style.color = 'red';
  } finally {
    nextBtn.disabled = false;
  }

}

// Handle display metrics changes (DPI / monitor moves)
if (window.electronAPI && window.electronAPI.onDisplayMetricsChanged) {
  window.electronAPI.onDisplayMetricsChanged(() => {
    // Recompute any CSS scaling if needed. For now, we rely on Electron/browser scaling.
    // If you want to adjust font sizes or redraw canvas, do it here.
    console.log('Display metrics changed - consider reflowing UI if needed.');
  });
  window.electronAPI.onWindowMoved(() => {
    console.log('Window moved - consider checking devicePixelRatio.');
  });
}