// 사이드바 네비게이션 active 상태 토글 + 부드러운 스크롤
document.querySelectorAll('.nav-item').forEach((item) => {
  item.addEventListener('click', (e) => {
    document.querySelectorAll('.nav-item').forEach((n) => n.classList.remove('active'));
    item.classList.add('active');
  });
});
