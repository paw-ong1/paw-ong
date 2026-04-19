import json
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from utils.file_loader import load_resource


def _load_dogs() -> list[dict]:
    """CSV에서 강아지 데이터를 로드하고 JS 호환 형태로 변환."""
    df = pd.read_csv("data/korea_dog_list_fixed.csv", encoding="utf-8-sig")

    activity_map = {1: "낮음", 2: "낮음", 3: "보통", 4: "높음", 5: "높음"}
    status_options = ["입양가능", "입양가능", "입양가능", "임시보호중"]

    dogs = []
    for idx, row in df.iterrows():
        original_id = str(row["아이디"])
        dogs.append({
            "id": idx + 1,
            "origId": original_id,
            "name": str(row["이름"]),
            "breed": str(row["품종"]),
            "age": max(1, int(row["나이(월)"]) // 12) if int(row["나이(월)"]) >= 12 else 1,
            "ageMonth": int(row["나이(월)"]),
            "gender": str(row["성별"]),
            "region": str(row["지역"]),
            "size": str(row["크기"]),
            "activity": activity_map.get(int(row["활동성"]), "보통"),
            "status": status_options[idx % len(status_options)],
            "color": str(row["색상1"]),
            "description": str(row.get("상세설명", "")),
            "vaccination": str(row["예방접종"]),
            "neutered": str(row["중성화"]),
        })
    return dogs


def _load_shelters() -> dict:
    """보호소 매핑 JSON 로드."""
    with open("data/shelter_info.json", "r", encoding="utf-8") as f:
        return json.load(f)


def render():
    css_content = load_resource("css/style.css")

    dogs = _load_dogs()
    shelters = _load_shelters()
    dogs_json = json.dumps(dogs, ensure_ascii=False)
    shelters_json = json.dumps(shelters, ensure_ascii=False)

    # Streamlit 서버의 static 이미지 base URL
    img_base = "app/static/dogs"

    html_code = f"""
    <style>{css_content}</style>
    <style>
    /* ── 카드형 리스트 ─────────────────────────────────── */
    .dog-card-list {{
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;
    }}
    .dog-list-card {{
      display: flex;
      gap: 18px;
      background: white;
      border-radius: 14px;
      padding: 14px;
      border: 1px solid #F0E4DC;
      box-shadow: 0 2px 8px rgba(0,0,0,0.04);
      cursor: pointer;
      transition: transform 0.15s, box-shadow 0.15s;
      align-items: center;
    }}
    .dog-list-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }}
    .dog-list-photo {{
      width: 120px;
      height: 120px;
      border-radius: 12px;
      object-fit: cover;
      flex-shrink: 0;
      border: 2px solid #F0E4DC;
    }}
    .dog-list-info {{
      flex: 1;
      min-width: 0;
    }}
    .dog-list-top {{
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 6px;
    }}
    .dog-list-name {{
      font-family: 'Gowun Batang', serif;
      font-size: 17px;
      font-weight: 700;
      color: #3D2B1F;
    }}
    .dog-list-details {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px 16px;
      font-size: 13px;
      color: #5C4535;
      margin-bottom: 6px;
    }}
    .dog-list-details span {{
      display: inline-flex;
      align-items: center;
      gap: 3px;
    }}
    .dog-list-desc {{
      font-size: 12px;
      color: #8B6555;
      line-height: 1.5;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      max-width: 500px;
    }}


    /* ── 상세 패널 ──────────────────────────────────────── */
    .dog-detail-overlay {{
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(61,43,31,0.45);
      z-index: 1000;
      justify-content: center;
      align-items: center;
    }}
    .dog-detail-overlay.show {{ display: flex; }}
    .dog-detail-panel {{
      background: #FDF6F0;
      border-radius: 20px;
      padding: 28px;
      max-width: 520px;
      width: 90%;
      max-height: 80vh;
      overflow-y: auto;
      box-shadow: 0 8px 40px rgba(0,0,0,0.15);
      position: relative;
    }}
    .detail-close {{
      position: absolute;
      top: 14px; right: 18px;
      background: none; border: none;
      font-size: 22px; cursor: pointer;
      color: #8B6555;
    }}
    .detail-close:hover {{ color: #3D2B1F; }}
    .detail-photo {{
      width: 100%;
      border-radius: 14px;
      margin-bottom: 18px;
      border: 2px solid #F0E4DC;
    }}
    .detail-header {{
      display: flex;
      align-items: center;
      gap: 16px;
      margin-bottom: 18px;
    }}
    .detail-name {{
      font-family: 'Gowun Batang', serif;
      font-size: 22px;
      font-weight: 700;
      color: #3D2B1F;
    }}
    .detail-breed {{ font-size: 13px; color: #8B6555; }}
    .detail-info-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
      margin-bottom: 18px;
    }}
    .detail-info-item {{
      background: white;
      border-radius: 10px;
      padding: 10px 14px;
      border: 1px solid #F0E4DC;
    }}
    .detail-info-label {{ font-size: 11px; color: #A08070; margin-bottom: 2px; }}
    .detail-info-value {{ font-size: 14px; font-weight: 600; color: #3D2B1F; }}
    .detail-desc {{
      background: #F5F0EC;
      border-radius: 12px;
      padding: 14px;
      font-size: 13px;
      color: #5C4535;
      line-height: 1.7;
      margin-bottom: 18px;
    }}
    .detail-shelter {{
      background: white;
      border-radius: 14px;
      padding: 16px;
      border: 1px solid #F0E4DC;
      margin-bottom: 14px;
    }}
    .detail-shelter-title {{
      font-family: 'Gowun Batang', serif;
      font-size: 15px;
      font-weight: 700;
      color: #3D2B1F;
      margin-bottom: 10px;
    }}
    .detail-shelter-name {{ font-size: 14px; font-weight: 600; color: #E8A598; margin-bottom: 4px; }}
    .detail-shelter-addr {{ font-size: 12px; color: #5C4535; margin-bottom: 4px; }}
    .detail-shelter-tel {{ font-size: 12px; color: #8B6555; }}
    .detail-map {{
      width: 100%;
      height: 200px;
      border-radius: 12px;
      border: 1px solid #F0E4DC;
      overflow: hidden;
    }}
    .detail-map iframe {{ width: 100%; height: 100%; border: none; }}

    /* ── 필터 ──────────────────────────────────────────── */
    .filter-select-region {{
      padding: 9px 12px;
      border: 1px solid #E8D5C4;
      border-radius: 10px;
      font-size: 13px;
      font-family: 'Noto Sans KR', sans-serif;
      color: #3D2B1F;
      background: white;
      outline: none;
      cursor: pointer;
    }}
    .filter-group {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}
    .filter-label {{
      font-size: 11px;
      font-weight: 600;
      color: #8B6555;
      padding-left: 4px;
    }}
    .result-count {{
      font-size: 13px;
      color: #3D2B1F;
      margin-bottom: 10px;
    }}
    .result-count strong {{ color: #E8A598; }}
    .result-filter-tag {{ color: #7D4F5A; font-weight: 600; }}
    </style>

    <!-- 상세 패널 오버레이 -->
    <div class="dog-detail-overlay" id="dog-detail-overlay" onclick="closeDetail(event)">
      <div class="dog-detail-panel" onclick="event.stopPropagation()">
        <button class="detail-close" onclick="document.getElementById('dog-detail-overlay').classList.remove('show')">&times;</button>
        <div id="dog-detail-content"></div>
      </div>
    </div>

    <section id="page-list" class="page active">
      <div class="paw-bg">🐾</div>
      <div class="page-title">현재 반려견 리스트 🩷</div>
      <div class="page-sub">보호소에서 기다리는 친구들을 만나보세요</div>

      <div class="filters">
        <input id="search-input" class="filter-input" type="text" placeholder="🔍  이름 또는 품종 검색...">
        <div class="filter-group">
          <span class="filter-label">상태</span>
          <select id="filter-status" class="filter-select">
            <option>전체</option>
            <option>입양가능</option>
            <option>임시보호중</option>
          </select>
        </div>
        <div class="filter-group">
          <span class="filter-label">크기</span>
          <select id="filter-size" class="filter-select">
            <option>전체</option>
            <option>소형</option>
            <option>중형</option>
            <option>대형</option>
          </select>
        </div>
        <div class="filter-group">
          <span class="filter-label">활동성</span>
          <select id="filter-act" class="filter-select">
            <option>전체</option>
            <option>낮음</option>
            <option>보통</option>
            <option>높음</option>
          </select>
        </div>
        <div class="filter-group">
          <span class="filter-label">지역</span>
          <select id="filter-region" class="filter-select-region">
            <option>전체 지역</option>
            <option>서울</option><option>경기</option><option>부산</option>
            <option>인천</option><option>대구</option><option>대전</option>
            <option>광주</option><option>울산</option><option>세종</option>
            <option>강원</option><option>충북</option><option>충남</option>
            <option>전북</option><option>전남</option><option>경북</option>
            <option>경남</option><option>제주</option>
          </select>
        </div>
      </div>

      <div class="result-count" id="result-count"></div>

      <div class="dog-card-list" id="dog-card-list"></div>

      <div class="pagination" id="pagination"></div>
    </section>

    <script>
    'use strict';
    const DOGS = {dogs_json};
    const SHELTERS = {shelters_json};
    const IMG_BASE = window.parent.location.origin + '/{img_base}/';

    let listPage = 1;
    const PAGE_SIZE = 8;
    let filteredDogs = [...DOGS];

    const STATUS_COLOR = {{ '입양가능':'badge-apricot', '임시보호중':'badge-green', '입양완료':'badge-gray' }};
    const SIZE_ICON = {{ '소형':'🐩', '중형':'🐕', '대형':'🦮' }};

    function getImgUrl(origId) {{
      return IMG_BASE + origId + '-1.jpg';
    }}

    function renderCards() {{
      const container = document.getElementById('dog-card-list');
      const info = document.getElementById('result-count');
      const total = filteredDogs.length;
      const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));
      listPage = Math.min(listPage, totalPages);

      const start = (listPage - 1) * PAGE_SIZE;
      const paged = filteredDogs.slice(start, start + PAGE_SIZE);

      // 결과 카운트 + 필터 태그
      if (info) {{
        const status = document.getElementById('filter-status')?.value || '전체';
        const size = document.getElementById('filter-size')?.value || '전체';
        const act = document.getElementById('filter-act')?.value || '전체';
        const region = document.getElementById('filter-region')?.value || '전체 지역';
        const search = document.getElementById('search-input')?.value || '';

        let tags = [];
        if (search) tags.push('검색: ' + search);
        if (status !== '전체') tags.push('상태: ' + status);
        if (size !== '전체') tags.push('크기: ' + size);
        if (act !== '전체') tags.push('활동성: ' + act);
        if (region !== '전체 지역') tags.push('지역: ' + region);

        if (tags.length === 0) {{
          info.innerHTML = '🐕 총 <strong>' + DOGS.length + '</strong>마리';
        }} else {{
          info.innerHTML = '🐕 ' + DOGS.length + '마리 중 <strong>' + total + '</strong>마리 | <span class="result-filter-tag">' + tags.join('&nbsp;&nbsp;') + '</span>';
        }}
      }}

      if (!container) return;
      container.innerHTML = paged.map(d => `
        <div class="dog-list-card" onclick="showDetail(${{d.id}})">
          <img class="dog-list-photo"
               src="${{getImgUrl(d.origId)}}"
               alt="${{d.name}}"
               loading="lazy"
               onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 120 120%22><rect fill=%22%23FDE8E4%22 width=%22120%22 height=%22120%22/><text x=%2260%22 y=%2270%22 text-anchor=%22middle%22 font-size=%2248%22>🐕</text></svg>'">
          <div class="dog-list-info">
            <div class="dog-list-top">
              <span class="dog-list-name">${{d.name}}</span>
              <span class="badge ${{STATUS_COLOR[d.status]}}">${{d.status}}</span>
            </div>
            <div class="dog-list-details">
              <span>🐾 ${{d.breed}}</span>
              <span>📅 ${{d.ageMonth}}개월</span>
              <span>${{d.gender === '수컷' ? '♂' : '♀'}} ${{d.gender}}</span>
              <span>${{SIZE_ICON[d.size] || ''}} ${{d.size}}</span>
              <span>📍 ${{d.region}}</span>
            </div>
            ${{d.description ? '<div class="dog-list-desc">' + d.description + '</div>' : ''}}
          </div>
        </div>
      `).join('');

      renderPagination(totalPages);
    }}

    function renderPagination(totalPages) {{
      const pag = document.getElementById('pagination');
      if (!pag) return;

      const maxVisible = 5;
      let startPage = Math.max(1, listPage - Math.floor(maxVisible / 2));
      let endPage = Math.min(totalPages, startPage + maxVisible - 1);
      if (endPage - startPage < maxVisible - 1) startPage = Math.max(1, endPage - maxVisible + 1);

      let html = '<button class="btn-pag" onclick="changePage(1)" ' + (listPage <= 1 ? 'disabled' : '') + '>◀◀</button>';
      html += '<button class="btn-pag" onclick="changePage(' + (listPage - 1) + ')" ' + (listPage <= 1 ? 'disabled' : '') + '>◀</button>';
      for (let p = startPage; p <= endPage; p++) {{
        html += '<button class="btn-pag ' + (p === listPage ? 'current' : '') + '" onclick="changePage(' + p + ')">' + p + '</button>';
      }}
      html += '<button class="btn-pag" onclick="changePage(' + (listPage + 1) + ')" ' + (listPage >= totalPages ? 'disabled' : '') + '>▶</button>';
      html += '<button class="btn-pag" onclick="changePage(' + totalPages + ')" ' + (listPage >= totalPages ? 'disabled' : '') + '>▶▶</button>';
      pag.innerHTML = html;
    }}

    function changePage(p) {{
      const totalPages = Math.ceil(filteredDogs.length / PAGE_SIZE);
      if (p < 1 || p > totalPages) return;
      listPage = p;
      renderCards();
    }}

    function applyFilters() {{
      const search = (document.getElementById('search-input')?.value || '').toLowerCase();
      const status = document.getElementById('filter-status')?.value || '전체';
      const size = document.getElementById('filter-size')?.value || '전체';
      const act = document.getElementById('filter-act')?.value || '전체';
      const region = document.getElementById('filter-region')?.value || '전체 지역';

      filteredDogs = DOGS.filter(d => {{
        const matchSearch = !search || d.name.toLowerCase().includes(search) || d.breed.toLowerCase().includes(search);
        const matchStatus = status === '전체' || d.status === status;
        const matchSize = size === '전체' || d.size === size;
        const matchAct = act === '전체' || d.activity === act;
        const matchRegion = region === '전체 지역' || d.region === region;
        return matchSearch && matchStatus && matchSize && matchAct && matchRegion;
      }});

      listPage = 1;
      renderCards();
    }}

    function showDetail(dogId) {{
      const dog = DOGS.find(d => d.id === dogId);
      if (!dog) return;

      const shelter = SHELTERS[dog.region];
      const content = document.getElementById('dog-detail-content');

      let shelterHtml = '';
      if (shelter) {{
        shelterHtml = `
          <div class="detail-shelter">
            <div class="detail-shelter-title">📍 보호소 정보</div>
            <div class="detail-shelter-name">${{shelter.name}}</div>
            <div class="detail-shelter-addr">📌 ${{shelter.address}}</div>
            <div class="detail-shelter-tel">📞 ${{shelter.tel}}</div>
          </div>
          <div class="detail-map">
            <iframe src="https://maps.google.com/maps?q=${{shelter.lat}},${{shelter.lng}}&z=14&output=embed" allowfullscreen></iframe>
          </div>
        `;
      }}

      content.innerHTML = `
        <img class="detail-photo" src="${{getImgUrl(dog.origId)}}" alt="${{dog.name}}"
             onerror="this.style.display='none'">
        <div class="detail-header">
          <div>
            <div class="detail-name">${{dog.name}}</div>
            <div class="detail-breed">${{dog.breed}} · <span class="badge ${{STATUS_COLOR[dog.status]}}">${{dog.status}}</span></div>
          </div>
        </div>
        <div class="detail-info-grid">
          <div class="detail-info-item">
            <div class="detail-info-label">나이</div>
            <div class="detail-info-value">${{dog.ageMonth}}개월</div>
          </div>
          <div class="detail-info-item">
            <div class="detail-info-label">성별</div>
            <div class="detail-info-value">${{dog.gender}}</div>
          </div>
          <div class="detail-info-item">
            <div class="detail-info-label">크기</div>
            <div class="detail-info-value">${{SIZE_ICON[dog.size] || ''}} ${{dog.size}}</div>
          </div>
          <div class="detail-info-item">
            <div class="detail-info-label">색상</div>
            <div class="detail-info-value">${{dog.color}}</div>
          </div>
          <div class="detail-info-item">
            <div class="detail-info-label">예방접종</div>
            <div class="detail-info-value">${{dog.vaccination}}</div>
          </div>
          <div class="detail-info-item">
            <div class="detail-info-label">중성화</div>
            <div class="detail-info-value">${{dog.neutered}}</div>
          </div>
        </div>
        ${{dog.description ? '<div class="detail-desc">' + dog.description + '</div>' : ''}}
        ${{shelterHtml}}
      `;

      document.getElementById('dog-detail-overlay').classList.add('show');
    }}

    function closeDetail(event) {{
      if (event.target === document.getElementById('dog-detail-overlay')) {{
        document.getElementById('dog-detail-overlay').classList.remove('show');
      }}
    }}

    document.addEventListener('DOMContentLoaded', () => {{
      ['search-input', 'filter-status', 'filter-size', 'filter-act', 'filter-region'].forEach(id => {{
        const el = document.getElementById(id);
        if (el) el.addEventListener('input', applyFilters);
        if (el) el.addEventListener('change', applyFilters);
      }});
      renderCards();
    }});
    </script>
    """

    components.html(html_code, height=1600)
