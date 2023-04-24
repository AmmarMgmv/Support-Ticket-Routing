const input = document.querySelector('.input-container.textarea textarea');
const label = document.querySelector('.input-container.textarea label');

input.addEventListener('focus', () => {
  label.classList.add('hidden');
});

input.addEventListener('blur', () => {
  if (input.value === '') {
    label.classList.remove('hidden');
  }
});