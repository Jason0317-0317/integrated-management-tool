// 全局狀態
let currentState = {
    role: null,
    feature: null,
    data: {}
};

const API_BASE = 'http://localhost:5000/api';

// 選擇身份
function selectRole(role) {
    currentState.role = role;
    showStep('feature');
    updateFeatureStep();
}

// 選擇功能
function selectFeature(feature) {
    currentState.feature = feature;
    showStep('function');
    loadFunction(feature);
}

// 返回上一步
function goBack() {
    if (currentState.feature) {
        currentState.feature = null;
        showStep('feature');
    } else if (currentState.role) {
        currentState.role = null;
        currentState.feature = null;
        showStep('role');
    }
}

// 顯示指定步驟
function showStep(step) {
    document.querySelectorAll('.step-container').forEach(el => {
        el.classList.remove('active');
    });
    document.getElementById(`step-${step}`).classList.add('active');
}

// 更新功能選擇步驟
function updateFeatureStep() {
    const title = currentState.role === 'manager' ? '店長功能選擇' : '小編功能選擇';
    document.getElementById('feature-title').textContent = title;

    const buttonsContainer = document.getElementById('feature-buttons');
    buttonsContainer.innerHTML = '';
    buttonsContainer.className = 'button-group grid';

    if (currentState.role === 'manager') {
        const features = [
            { id: 'lesson_report', label: '教練堂數統計' },
            { id: 'sales_report', label: '團個績計算工具' },
            { id: 'attendance_report', label: '出勤明細統計' }
        ];
        features.forEach(feature => {
            const btn = document.createElement('button');
            btn.className = 'btn btn-primary';
            btn.textContent = feature.label;
            btn.onclick = () => selectFeature(feature.id);
            buttonsContainer.appendChild(btn);
        });
    } else {
        const btn = document.createElement('button');
        btn.className = 'btn btn-secondary';
        btn.textContent = '業務獎金計算';
        btn.onclick = () => selectFeature('editor_bonus');
        btn.style.width = '100%';
        buttonsContainer.appendChild(btn);
    }
}

// 載入功能頁面
function loadFunction(feature) {
    const contentDiv = document.getElementById('function-content');
    const titleDiv = document.getElementById('function-title');

    if (feature === 'lesson_report') {
        titleDiv.textContent = '預約報表自動統計系統';
        contentDiv.innerHTML = `
            <div class="form-group">
                <p style="color: #666; margin-bottom: 20px;">請上傳原始團體課預約報表，系統將自動提取並整理為指定格式。</p>
            </div>

            <h3 style="margin-top: 30px; margin-bottom: 15px;">1. 設定篩選條件</h3>
            <div class="form-row">
                <div class="form-group">
                    <label for="branch">選擇館別</label>
                    <select id="branch">
                        <option>全部</option>
                        <option>中山館</option>
                        <option>高美館</option>
                        <option>義昌館</option>
                        <option>巨蛋館</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="start-date">開始日期</label>
                    <input type="date" id="start-date">
                </div>
            </div>
            <div class="form-group">
                <label for="end-date">結束日期</label>
                <input type="date" id="end-date">
            </div>

            <h3 style="margin-top: 30px; margin-bottom: 15px;">2. 上傳報表檔案</h3>
            <div class="form-group">
                <label for="lesson-file">選擇原始檔案 (Excel 或 CSV)</label>
                <input type="file" id="lesson-file" accept=".xlsx,.xls,.csv">
            </div>

            <button class="btn btn-primary" onclick="processLessonReport()" style="margin-top: 20px;">
                處理報表
            </button>

            <div id="lesson-result"></div>
        `;

        // 設置默認日期
        const today = new Date();
        const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
        document.getElementById('start-date').valueAsDate = firstDay;
        document.getElementById('end-date').valueAsDate = today;

    } else if (feature === 'sales_report') {
        titleDiv.textContent = '業績報表自動化轉換工具';
        contentDiv.innerHTML = `
            <div class="form-group">
                <p style="color: #666; margin-bottom: 20px;">請上傳原始交易報表，系統將自動提取並整理為指定格式。</p>
            </div>

            <div class="form-group">
                <label for="sales-file">選擇原始 Excel 檔案</label>
                <input type="file" id="sales-file" accept=".xlsx">
            </div>

            <button class="btn btn-primary" onclick="processSalesReport()" style="margin-top: 20px;">
                處理報表
            </button>

            <div id="sales-result"></div>
        `;

     } else if (feature === 'editor_bonus') {
        titleDiv.textContent = '業務獎金計算系統';
        contentDiv.innerHTML = `
            <h3 style="margin-top: 20px; margin-bottom: 15px;">基本資訊設定</h3>
            <div class="form-row">
                <div class="form-group">
                    <label for="gym">館別</label>
                    <select id="gym">
                        <option>巨蛋館</option>
                        <option>其他分館</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="editor-name">小編姓名</label>
                    <input type="text" id="editor-name" placeholder="請輸入姓名">
                </div>
                <div class="form-group">
                    <label for="report-date">報表日期</label>
                    <input type="date" id="report-date">
                </div>
                <div class="form-group">
                    <label for="employment-type">員工身份</label>
                    <select id="employment-type">
                        <option value="full-time">正職</option>
                        <option value="part-time">兼職</option>
                    </select>
                </div>
            </div>

            <h3 style="margin-top: 40px; margin-bottom: 15px; border-top: 2px solid #e5e7eb; padding-top: 30px;">1. 體驗與品牌推廣</h3>
            <div class="form-group">
                <label for="revenue-tier">個人業績獎金級別</label>
                <select id="revenue-tier" onchange="updateBonusCalculation()">
                    <option value="none">不列入計算</option>
                    <option value="120000">12萬元</option>
                    <option value="240000">24萬元</option>
                    <option value="300000">30萬元</option>
                </select>
            </div>

            <div class="form-row">
                <div class="form-group">
                    <label for="deal-today">當天成交(筆)</label>
                    <input type="number" id="deal-today" value="0" min="0" onchange="updateBonusCalculation()">
                </div>
                <div class="form-group">
                    <label for="deal-48h">48小時(筆)</label>
                    <input type="number" id="deal-48h" value="0" min="0" onchange="updateBonusCalculation()">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="deal-7d">7天內(筆)</label>
                    <input type="number" id="deal-7d" value="0" min="0" onchange="updateBonusCalculation()">
                </div>
                <div class="form-group">
                    <label for="deal-over7">超過7天(筆)</label>
                    <input type="number" id="deal-over7" value="0" min="0" onchange="updateBonusCalculation()">
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="brand-count">品牌推廣人數</label>
                    <input type="number" id="brand-count" value="5" min="0" onchange="updateBonusCalculation()">
                </div>
                <div class="form-group">
                    <label for="extra-classes">補開課程次數</label>
                    <input type="number" id="extra-classes" value="0" min="0" onchange="updateBonusCalculation()">
                </div>
            </div>

            <h3 style="margin-top: 30px; margin-bottom: 15px;">2. 回流與升級項目</h3>
            <div class="form-row">
                <div>
                    <h4 style="margin-bottom: 15px;">回流人數 (STP-T)</h4>
                    <div class="form-group">
                        <label for="loyalty-10">10堂人數</label>
                        <input type="number" id="loyalty-10" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                    <div class="form-group">
                        <label for="loyalty-20">20堂人數</label>
                        <input type="number" id="loyalty-20" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                    <div class="form-group">
                        <label for="loyalty-30">30堂人數</label>
                        <input type="number" id="loyalty-30" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                    <div class="form-group">
                        <label for="loyalty-40">40堂人數</label>
                        <input type="number" id="loyalty-40" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                </div>
                <div>
                    <h4 style="margin-bottom: 15px;">結構升級次數</h4>
                    <div class="form-group">
                        <label for="upgrade-1213">1對2變1對3(次)</label>
                        <input type="number" id="upgrade-1213" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                    <div class="form-group">
                        <label for="upgrade-group">團課變期班(次)</label>
                        <input type="number" id="upgrade-group" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                    <div class="form-group">
                        <label for="upgrade-class">包班成立(次)</label>
                        <input type="number" id="upgrade-class" value="0" min="0" onchange="updateBonusCalculation()">
                    </div>
                </div>
            </div>

            <div id="bonus-result"></div>

            <button class="btn btn-primary" onclick="downloadBonusReport()" style="margin-top: 20px;">
                產生並下載結算報表
            </button>
        `;

        // 設置默認日期
        const reportDateInput = document.getElementById('report-date');
        if (reportDateInput) {
            reportDateInput.valueAsDate = new Date();
        }
        updateBonusCalculation();
    }
}

// 處理預約報表
async function processLessonReport() {
    const fileInput = document.getElementById('lesson-file');
    const resultDiv = document.getElementById('lesson-result');

    if (!fileInput.files.length) {
        resultDiv.innerHTML = '<div class="alert alert-error">請選擇檔案</div>';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('branch', document.getElementById('branch').value);
    formData.append('start_date', document.getElementById('start-date').value);
    formData.append('end_date', document.getElementById('end-date').value);

    resultDiv.innerHTML = '<div class="alert alert-info">處理中...</div>';

    try {
        const response = await fetch(`${API_BASE}/process-lesson-report`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">檔案處理成功</div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>課程項目</th>
                                ${data.teachers.map(t => `<th>${t}</th>`).join('')}
                                <th>合計</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${data.stats.map(row => `
                                <tr>
                                    <td>${row.course}</td>
                                    ${row.values.map(v => `<td>${v}</td>`).join('')}
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>
                </div>
                <button class="btn btn-download" onclick="downloadFile('lesson-report')">
                    下載 Excel 報表
                </button>
            `;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-error">${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-error">處理失敗: ${error.message}</div>`;
    }
}

// 處理業績報表
async function processSalesReport() {
    const fileInput = document.getElementById('sales-file');
    const resultDiv = document.getElementById('sales-result');

    if (!fileInput.files.length) {
        resultDiv.innerHTML = '<div class="alert alert-error">請選擇檔案</div>';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    resultDiv.innerHTML = '<div class="alert alert-info">處理中...</div>';

    try {
        const response = await fetch(`${API_BASE}/process-sales-report`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            resultDiv.innerHTML = `
                <div class="alert alert-success">檔案處理成功</div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                    <div>
                        <h4 style="margin-bottom: 10px;">新購預覽</h4>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>業績人員</th>
                                        <th>會員姓名</th>
                                        <th>金額</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.new_sales.slice(0, 5).map(row => `
                                        <tr>
                                            <td>${row.salesperson}</td>
                                            <td>${row.member}</td>
                                            <td>${row.amount}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                    <div>
                        <h4 style="margin-bottom: 10px;">續購預覽</h4>
                        <div class="table-container">
                            <table>
                                <thead>
                                    <tr>
                                        <th>業績人員</th>
                                        <th>會員姓名</th>
                                        <th>金額</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${data.renew_sales.slice(0, 5).map(row => `
                                        <tr>
                                            <td>${row.salesperson}</td>
                                            <td>${row.member}</td>
                                            <td>${row.amount}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
                <button class="btn btn-download" onclick="downloadFile('sales-report')">
                    下載轉換後的 Excel 報表
                </button>
            `;
        } else {
            resultDiv.innerHTML = `<div class="alert alert-error">${data.error}</div>`;
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-error">處理失敗: ${error.message}</div>`;
    }
}

// 更新獎金計算
function updateBonusCalculation() {
    const dealToday = parseInt(document.getElementById('deal-today').value) || 0;
    const deal48h = parseInt(document.getElementById('deal-48h').value) || 0;
    const deal7d = parseInt(document.getElementById('deal-7d').value) || 0;
    const dealOver7 = parseInt(document.getElementById('deal-over7').value) || 0;
    const brandCount = parseInt(document.getElementById('brand-count').value) || 0;
    const extraClasses = parseInt(document.getElementById('extra-classes').value) || 0;
    const loyalty10 = parseInt(document.getElementById('loyalty-10').value) || 0;
    const loyalty20 = parseInt(document.getElementById('loyalty-20').value) || 0;
    const loyalty30 = parseInt(document.getElementById('loyalty-30').value) || 0;
    const loyalty40 = parseInt(document.getElementById('loyalty-40').value) || 0;
    const upgrade1213 = parseInt(document.getElementById('upgrade-1213').value) || 0;
    const upgradeGroup = parseInt(document.getElementById('upgrade-group').value) || 0;
    const upgradeClass = parseInt(document.getElementById('upgrade-class').value) || 0;
    const revenueTier = document.getElementById('revenue-tier').value;
    const isFullTime = document.getElementById('employment-type').value === 'full-time';

    // 計算各項獎金
    const dealBonus = dealToday * 80 + deal48h * 60 + deal7d * 50 + dealOver7 * 0;
    const classBonus = extraClasses * 30;
    const loyaltyBonus = loyalty10 * 100 + loyalty20 * 200 + loyalty30 * 300 + loyalty40 * 500;
    const upgradeBonus = upgrade1213 * 100 + upgradeGroup * 150 + upgradeClass * 300;

    // 品牌知名度獎金
    const baseVal = isFullTime ? 5 : 2;
    let brandBonus = 0;
    let brandNote = '';
    if (brandCount === 0) {
        brandBonus = -200;
        brandNote = '推廣人數為 0';
    } else if (brandCount < baseVal) {
        brandBonus = -100;
        brandNote = `未達門檻 (${baseVal}位)`;
    } else if (brandCount === baseVal) {
        brandBonus = 0;
        brandNote = '符合基本門檻';
    } else {
        const extraUnits = Math.floor((brandCount - baseVal) / 5);
        brandBonus = extraUnits * 200;
        brandNote = `加發 ${extraUnits} 組獎金`;
    }

    // 月高手獎勵
    const totalDeals = dealToday + deal48h + deal7d + dealOver7 + upgrade1213 + upgradeGroup + upgradeClass + loyalty10 + loyalty20 + loyalty30 + loyalty40 + extraClasses;
    let monthlyBonus = 0;
    if (totalDeals >= 50) {
        monthlyBonus = 5000;
    } else if (totalDeals >= 30) {
        monthlyBonus = 2000;
    }

    // 個人業績獎金
    const revenueBonus = {
        'none': 0,
        '120000': 2000,
        '240000': 4000,
        '300000': 6000
    }[revenueTier] || 0;

    const totalBonus = dealBonus + classBonus + loyaltyBonus + upgradeBonus + brandBonus + monthlyBonus + revenueBonus;

    // 顯示結果
    const resultDiv = document.getElementById('bonus-result');
    resultDiv.innerHTML = `
        <div class="metric">
            <div class="metric-label">當月預計總獎金</div>
            <div class="metric-value">${totalBonus} 元</div>
        </div>
    `;
}

// 下載報表
function downloadFile(type) {
    // 這會在後端實現
    window.location.href = `${API_BASE}/download-${type}`;
}

// 下載獎金報表
function downloadBonusReport() {
    const data = {
        gym: document.getElementById('gym').value,
        name: document.getElementById('editor-name').value,
        date: document.getElementById('report-date').value,
        employment_type: document.getElementById('employment-type').value,
        revenue_tier: document.getElementById('revenue-tier').value,
        deal_today: parseInt(document.getElementById('deal-today').value) || 0,
        deal_48h: parseInt(document.getElementById('deal-48h').value) || 0,
        deal_7d: parseInt(document.getElementById('deal-7d').value) || 0,
        deal_over7: parseInt(document.getElementById('deal-over7').value) || 0,
        brand_count: parseInt(document.getElementById('brand-count').value) || 0,
        extra_classes: parseInt(document.getElementById('extra-classes').value) || 0,
        loyalty_10: parseInt(document.getElementById('loyalty-10').value) || 0,
        loyalty_20: parseInt(document.getElementById('loyalty-20').value) || 0,
        loyalty_30: parseInt(document.getElementById('loyalty-30').value) || 0,
        loyalty_40: parseInt(document.getElementById('loyalty-40').value) || 0,
        upgrade_1213: parseInt(document.getElementById('upgrade-1213').value) || 0,
        upgrade_group: parseInt(document.getElementById('upgrade-group').value) || 0,
        upgrade_class: parseInt(document.getElementById('upgrade-class').value) || 0
    };

    fetch(`${API_BASE}/download-bonus-report`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `${data.name}_獎金結算_${data.date}.xlsx`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    })
    .catch(error => alert('下載失敗: ' + error.message));
}
