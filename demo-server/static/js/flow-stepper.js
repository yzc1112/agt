// Flow stepper for slides with interactive data flow visualization
// Shared by step-01, step-02, step-03

function createFlowStepper(slideId) {
  const data = FLOW_DATA[slideId];
  if (!data) {
    console.error('createFlowStepper: no FLOW_DATA for', slideId);
    return;
  }

  let current = -1; // -1 = initial blank state (Step 0)

  function update() {
    // Build element ID suffix
    let suffix;
    if (slideId === 'step-03') {
      suffix = '';
    } else {
      suffix = slideId.replace('step-0', '0').replace('step-', '');
    }

    // Clear all highlights
    const containerId = suffix ? `flow-code-${suffix}` : 'flow-code';
    const container = document.getElementById(containerId);
    if (container) {
      container.querySelectorAll('.flow-line').forEach(el => {
        el.classList.remove('active');
        // Reset opacity based on dim attribute, or leave as is if no dim
        if (el.hasAttribute('data-dim')) {
          el.style.opacity = '';
        }
      });
    }

    // Hide all cards (up to 3)
    for (let i = 1; i <= 3; i++) {
      const card = document.getElementById((data.cards[i - 1] || {}).id);
      if (card) card.style.display = 'none';
    }

    // Apply current step (current=-1 means blank initial state)
    if (current >= 0 && current < data.steps.length) {
      const step = data.steps[current];
      step.lines.forEach(idx => {
        const el = document.getElementById(data.codeLines[idx].id);
        if (el) {
          el.classList.add('active');
          el.style.opacity = '1';
        }
      });
      if (step.card) {
        const card = document.getElementById(data.cards[step.card - 1].id);
        if (card) card.style.display = 'block';
      }
    }

    // Update label (display step number = current + 1, 0 = initial blank)
    const labelId = `flow${suffix}-step-label`;
    const label = document.getElementById(labelId);
    if (label) {
      label.textContent = 'Step ' + (current + 1) + ' / ' + data.steps.length;
    }

    // Update buttons
    const prevBtn = document.getElementById(`flow${suffix}-prev`);
    const nextBtn = document.getElementById(`flow${suffix}-next`);
    if (prevBtn) prevBtn.style.opacity = current === -1 ? '0.3' : '1';
    if (nextBtn) nextBtn.style.opacity = current === data.steps.length - 1 ? '0.3' : '1';
  }

  return function(direction) {
    const next = current + direction;
    if (next < -1 || next >= data.steps.length) return;
    current = next;
    update();
  };
}

// Initialize all flowSteppers when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  if (typeof flowStep !== 'undefined') {
    // step-03 already initialized in main script
  }
});