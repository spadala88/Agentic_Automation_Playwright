// Tab switching and interaction logic
document.addEventListener('DOMContentLoaded', () => {
  const tabs = document.querySelectorAll('[role="tab"]');
  const panels = document.querySelectorAll('[role="tabpanel"]');
  const statusIndicator = document.getElementById('active-tab-status');
  const clickCounter = document.getElementById('click-counter');
  const saveBtn = document.getElementById('btn-save-settings');
  const saveStatus = document.getElementById('save-status');

  let totalClicks = 0;

  function switchTab(newTab) {
    const targetPanelId = newTab.getAttribute('aria-controls');
    const tabName = newTab.getAttribute('data-tab');

    // Deselect all tabs
    tabs.forEach((tab) => {
      tab.classList.remove('active');
      tab.setAttribute('aria-selected', 'false');
    });

    // Hide all panels
    panels.forEach((panel) => {
      panel.classList.remove('active');
      panel.hidden = true;
    });

    // Activate clicked tab
    newTab.classList.add('active');
    newTab.setAttribute('aria-selected', 'true');

    // Show corresponding panel
    const targetPanel = document.getElementById(targetPanelId);
    if (targetPanel) {
      targetPanel.classList.add('active');
      targetPanel.hidden = false;
    }

    // Update status and counter
    const capitalizedName = tabName.charAt(0).toUpperCase() + tabName.slice(1);
    if (statusIndicator) {
      statusIndicator.textContent = `Active: ${capitalizedName}`;
    }

    totalClicks++;
    if (clickCounter) {
      clickCounter.textContent = totalClicks;
    }
  }

  // Attach click listeners to all tab buttons
  tabs.forEach((tab) => {
    tab.addEventListener('click', (e) => {
      switchTab(e.currentTarget);
    });

    // Keyboard support (Left / Right Arrow navigation)
    tab.addEventListener('keydown', (e) => {
      let index = Array.from(tabs).indexOf(e.currentTarget);
      if (e.key === 'ArrowRight') {
        const nextTab = tabs[(index + 1) % tabs.length];
        nextTab.focus();
        switchTab(nextTab);
      } else if (e.key === 'ArrowLeft') {
        const prevTab = tabs[(index - 1 + tabs.length) % tabs.length];
        prevTab.focus();
        switchTab(prevTab);
      }
    });
  });

  // Settings Save Button Demo
  if (saveBtn && saveStatus) {
    saveBtn.addEventListener('click', () => {
      saveStatus.textContent = 'Settings saved successfully! ✓';
      setTimeout(() => {
        saveStatus.textContent = '';
      }, 3000);
    });
  }
});
