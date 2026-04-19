'use strict';

/* ═══════════════════════════════════════════════════════════════════════════ */
/* 데이터                                                                        */
/* ═══════════════════════════════════════════════════════════════════════════ */
const DOGS = [
  { id:1,  name:'초코',   breed:'믹스견',       age:3, gender:'수컷', region:'서울 강남',   status:'입양가능',   size:'소형', activity:'보통' },
  { id:2,  name:'달이',   breed:'말티즈',       age:1, gender:'암컷', region:'부산 해운대', status:'입양가능',   size:'소형', activity:'낮음' },
  { id:3,  name:'쿠키',   breed:'포메라니안',   age:2, gender:'수컷', region:'서울 마포',   status:'임시보호중', size:'소형', activity:'높음' },
  { id:4,  name:'몽이',   breed:'비숑',         age:5, gender:'암컷', region:'인천 부평',   status:'입양가능',   size:'소형', activity:'낮음' },
  { id:5,  name:'하루',   breed:'진돗개',       age:4, gender:'수컷', region:'대전 유성',   status:'입양가능',   size:'중형', activity:'높음' },
  { id:6,  name:'별이',   breed:'치와와',       age:1, gender:'암컷', region:'서울 송파',   status:'입양완료',   size:'소형', activity:'낮음' },
  { id:7,  name:'토리',   breed:'시츄',         age:3, gender:'수컷', region:'경기 수원',   status:'입양가능',   size:'소형', activity:'보통' },
  { id:8,  name:'누리',   breed:'골든리트리버', age:2, gender:'암컷', region:'서울 노원',   status:'입양가능',   size:'대형', activity:'높음' },
  { id:9,  name:'해피',   breed:'닥스훈트',     age:6, gender:'수컷', region:'부산 사상',   status:'임시보호중', size:'소형', activity:'보통' },
  { id:10, name:'콩이',   breed:'푸들',         age:1, gender:'암컷', region:'대구 달서',   status:'입양가능',   size:'소형', activity:'낮음' },
  { id:11, name:'루나',   breed:'스피츠',       age:2, gender:'암컷', region:'서울 은평',   status:'입양가능',   size:'소형', activity:'보통' },
  { id:12, name:'모카',   breed:'코카스파니엘', age:4, gender:'수컷', region:'경기 성남',   status:'입양완료',   size:'중형', activity:'높음' },
  { id:13, name:'바둑이', breed:'허스키',       age:3, gender:'수컷', region:'인천 연수',   status:'입양가능',   size:'대형', activity:'높음' },
  { id:14, name:'솜이',   breed:'페키니즈',     age:7, gender:'암컷', region:'서울 강서',   status:'입양가능',   size:'소형', activity:'낮음' },
  { id:15, name:'뭉치',   breed:'말티즈',       age:1, gender:'수컷', region:'부산 동래',   status:'입양가능',   size:'소형', activity:'낮음' },
  { id:16, name:'보리',   breed:'비글',         age:2, gender:'수컷', region:'경기 안양',   status:'임시보호중', size:'중형', activity:'높음' },
  { id:17, name:'달콩',   breed:'포메라니안',   age:5, gender:'암컷', region:'서울 광진',   status:'입양가능',   size:'소형', activity:'보통' },
  { id:18, name:'나비',   breed:'믹스견',       age:3, gender:'암컷', region:'대전 서구',   status:'입양가능',   size:'중형', activity:'보통' },
  { id:19, name:'구름',   breed:'보더콜리',     age:2, gender:'수컷', region:'경기 고양',   status:'입양가능',   size:'대형', activity:'높음' },
  { id:20, name:'코코',   breed:'요크셔테리어', age:1, gender:'암컷', region:'서울 종로',   status:'입양완료',   size:'소형', activity:'낮음' },
];

const BREED_DB = {
  '골든 리트리버': { emoji:'🦮', activity:'높음', care:'매일 1시간 이상 산책 필요',   note:'털 빠짐 많음 — 정기 그루밍 필수' },
  '말티즈':        { emoji:'🐩', activity:'보통', care:'실내 활동으로도 충분',         note:'눈물 자국 관리 필요' },
  '포메라니안':    { emoji:'🐕', activity:'보통', care:'하루 30분 산책 권장',          note:'추위에 약함 — 보온 필수' },
  '비숑 프리제':   { emoji:'🐶', activity:'낮음', care:'실내 위주 생활 가능',          note:'정기 미용 필수 (저알레르기)' },
  '진돗개':        { emoji:'🦊', activity:'높음', care:'넓은 공간 & 충분한 운동',     note:'사회화 훈련이 중요' },
};

/* ═══════════════════════════════════════════════════════════════════════════ */
/* 네비게이션                                                                    */
/* ═══════════════════════════════════════════════════════════════════════════ */
function navigate(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));

  const page = document.getElementById('page-' + pageId);
  if (page) page.classList.add('active');

  const btn = document.querySelector(`.nav-btn[data-page="${pageId}"]`);
  if (btn) btn.classList.add('active');
}

/* ═══════════════════════════════════════════════════════════════════════════ */
/* PAGE 1 — 추천견 렌더링                                                        */
/* ═══════════════════════════════════════════════════════════════════════════ */
const FEATURED_EMOJIS  = ['🦮', '🐩', '🐕‍🦺'];
const FEATURED_COLORS  = ['#F2C4CE', '#C8E6C9', '#FDE8E4'];

function renderFeatured() {
  const available = DOGS.filter(d => d.status === '입양가능');
  const featured  = available.slice(0, 3);
  const container = document.getElementById('featured-dogs');
  if (!container) return;

  container.innerHTML = featured.map((d, i) => `
    <div class="dog-card">
      <div class="dog-card-img" style="background:${FEATURED_COLORS[i]}">${FEATURED_EMOJIS[i]}</div>
      <div class="dog-card-body">
        <div class="dog-card-name">${d.name}</div>
        <div class="dog-card-info">${d.breed} · ${d.age}살 · ${d.gender}</div>
        <div class="dog-card-region">📍 ${d.region}</div>
        <button class="dog-card-btn" onclick="navigate('list')">입양 신청 →</button>
      </div>
    </div>
  `).join('');
}

/* ═══════════════════════════════════════════════════════════════════════════ */
/* PAGE 2 — 반려견 리스트                                                        */
/* ═══════════════════════════════════════════════════════════════════════════ */
let listPage = 1;
const PAGE_SIZE = 8;
let filteredDogs = [...DOGS];

const STATUS_COLOR = { '입양가능':'badge-apricot', '임시보호중':'badge-green', '입양완료':'badge-gray' };
const SIZE_ICON    = { '소형':'🐩', '중형':'🐕', '대형':'🦮' };

function renderTable() {
  const tbody = document.getElementById('dog-tbody');
  const info  = document.getElementById('result-count');
  const total = filteredDogs.length;
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
  listPage = Math.min(listPage, totalPages);

  const start = (listPage - 1) * PAGE_SIZE;
  const paged = filteredDogs.slice(start, start + PAGE_SIZE);

  if (info) info.textContent = `총 ${DOGS.length}마리 중 ${total}마리 표시`;

  if (!tbody) return;
  tbody.innerHTML = paged.map(d => `
    <div class="table-row">
      <span class="table-id">${d.id}</span>
      <span class="table-name">${d.name}</span>
      <span>${d.breed}</span>
      <span>${d.age}살</span>
      <span>${d.gender}</span>
      <span class="table-region">📍 ${d.region}</span>
      <span><span class="badge ${STATUS_COLOR[d.status]}">${d.status}</span></span>
      <span>${SIZE_ICON[d.size]} ${d.size}</span>
    </div>
  `).join('');

  renderPagination(totalPages);
}

function renderPagination(totalPages) {
  const pag = document.getElementById('pagination');
  if (!pag) return;

  let html = `<button class="btn-pag" onclick="changePage(${listPage - 1})" ${listPage <= 1 ? 'disabled' : ''}>◀ 이전</button>`;
  for (let p = 1; p <= totalPages; p++) {
    html += `<button class="btn-pag ${p === listPage ? 'current' : ''}" onclick="changePage(${p})">${p}</button>`;
  }
  html += `<button class="btn-pag" onclick="changePage(${listPage + 1})" ${listPage >= totalPages ? 'disabled' : ''}>다음 ▶</button>`;
  pag.innerHTML = html;
}

function changePage(p) {
  const totalPages = Math.ceil(filteredDogs.length / PAGE_SIZE);
  if (p < 1 || p > totalPages) return;
  listPage = p;
  renderTable();
}

function applyFilters() {
  const search = document.getElementById('search-input')?.value.toLowerCase() || '';
  const status = document.getElementById('filter-status')?.value || '전체';
  const size   = document.getElementById('filter-size')?.value   || '전체';
  const act    = document.getElementById('filter-act')?.value    || '전체';

  filteredDogs = DOGS.filter(d => {
    const matchSearch = !search || d.name.includes(search) || d.breed.includes(search);
    const matchStatus = status === '전체' || d.status === status;
    const matchSize   = size   === '전체' || d.size   === size;
    const matchAct    = act    === '전체' || d.activity === act;
    return matchSearch && matchStatus && matchSize && matchAct;
  });

  listPage = 1;
  renderTable();
}

/* ═══════════════════════════════════════════════════════════════════════════ */
/* PAGE 3 — 퍼펙트 매칭                                                         */
/* ═══════════════════════════════════════════════════════════════════════════ */
function doMatch() {
  const housing  = document.querySelector('input[name="housing"]:checked')?.value  || 'apartment';
  const walk     = parseInt(document.getElementById('walk-slider')?.value || '1');
  const activity = document.querySelector('input[name="activity"]:checked')?.value || 'calm';
  const allergy  = document.querySelector('input[name="allergy"]:checked')?.value  || 'ok';
  const exp      = document.getElementById('experience')?.value || 'first';

  // 점수 계산
  let score = 75;
  if (housing === 'house')    score += 10;
  else if (housing === 'apt') score += 5;
  score += Math.min(walk * 3, 12);
  if (exp === '3years')   score += 5;
  else if (exp === '1-3') score += 3;
  score = Math.min(score, 99);

  // 품종 추천
  let breed, breedEmoji;
  if (activity === 'active' && walk >= 2) {
    breed = '골든 리트리버'; breedEmoji = '🦮';
  } else if (activity === 'calm' && allergy === 'sensitive') {
    breed = '비숑 프리제'; breedEmoji = '🐕';
  } else if (activity === 'calm') {
    breed = '말티즈'; breedEmoji = '🐩';
  } else {
    breed = '포메라니안'; breedEmoji = '🐕';
  }

  const housingLabel = { apartment:'아파트', house:'주택', officetel:'오피스텔' }[housing] || '';
  let reason = `'${breed}'는 ${housingLabel} 환경과 하루 ${walk}시간 산책에 최적화된 품종입니다.`;
  if (allergy === 'sensitive') reason += ' 저알레르기 품종으로 예민한 분께도 안성맞춤이에요.';

  showResult({ score, breed, breedEmoji, reason });
}

function showResult({ score, breed, breedEmoji, reason }) {
  // 빈 상태 숨기기
  const empty  = document.getElementById('result-empty');
  const panel  = document.getElementById('result-panel');
  if (empty) empty.style.display = 'none';
  if (panel) { panel.style.display = 'block'; }

  // 내용 채우기
  document.getElementById('res-emoji').textContent = breedEmoji;
  document.getElementById('res-score').textContent = '0% 일치!';
  document.getElementById('res-breed').innerHTML =
    `당신은 <strong>${breed}</strong>와<br>최고의 궁합입니다 🩷`;
  document.getElementById('res-reason').innerHTML =
    `🤖 <strong>AI 추천 이유</strong><br>${reason}`;

  // 점수 애니메이션
  let cur = 0;
  const interval = setInterval(() => {
    cur = Math.min(cur + 2, score);
    document.getElementById('res-score').textContent = `${cur}% 일치!`;
    if (cur >= score) clearInterval(interval);
  }, 18);

  // 바 차트 애니메이션
  const bars = [
    { id:'bar-activity', value: Math.min(score + 2, 99) },
    { id:'bar-housing',  value: Math.min(score - 4, 97) },
    { id:'bar-exp',      value: Math.min(score - 9, 95) },
  ];
  bars.forEach(b => {
    const el = document.getElementById(b.id + '-val');
    const fill = document.getElementById(b.id + '-fill');
    if (el) el.textContent = b.value + '%';
    setTimeout(() => {
      if (fill) fill.style.width = b.value + '%';
    }, 100);
  });
}

function updateWalkLabel(val) {
  const el = document.getElementById('walk-val');
  if (el) el.textContent = `${val}시간`;
}

/* ═══════════════════════════════════════════════════════════════════════════ */
/* PAGE 4 — 품종 가이드 & FAQ                                                   */
/* ═══════════════════════════════════════════════════════════════════════════ */
function updateBreedGuide(breedName) {
  const info = BREED_DB[breedName];
  if (!info) return;
  document.getElementById('breed-emoji').textContent = info.emoji;
  document.getElementById('breed-name-display').textContent = breedName;
  document.getElementById('breed-activity').textContent = info.activity;
  document.getElementById('breed-care').textContent = info.care;
  document.getElementById('breed-note').textContent = info.note;
}

function toggleFAQ(btn) {
  const isOpen = btn.classList.contains('open');
  // 모두 닫기
  document.querySelectorAll('.faq-q').forEach(q => q.classList.remove('open'));
  document.querySelectorAll('.faq-a').forEach(a => a.classList.remove('open'));
  // 클릭된 것만 열기 (토글)
  if (!isOpen) {
    btn.classList.add('open');
    btn.nextElementSibling.classList.add('open');
  }
}

/* ═══════════════════════════════════════════════════════════════════════════ */
/* 초기화                                                                        */
/* ═══════════════════════════════════════════════════════════════════════════ */
document.addEventListener('DOMContentLoaded', () => {
  // 네비게이션
  document.querySelectorAll('.nav-btn').forEach(btn => {
    btn.addEventListener('click', () => navigate(btn.dataset.page));
  });

  // Page 1
  renderFeatured();

  // Page 2 필터
  ['search-input', 'filter-status', 'filter-size', 'filter-act'].forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', applyFilters);
  });
  renderTable();

  // Page 4 품종 선택
  const breedSel = document.getElementById('breed-select');
  if (breedSel) {
    breedSel.addEventListener('change', () => updateBreedGuide(breedSel.value));
    updateBreedGuide(breedSel.value);
  }
});
