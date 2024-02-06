document.addEventListener('DOMContentLoaded', function() {
    const calendarEl = document.getElementById('calendar');
    const currentYearMonthEl = document.getElementById('current-year-month');
    let currentDate = new Date();


    function renderCalendar() {

        calendarEl.innerHTML = ''; // カレンダーをクリア
        let year = currentDate.getFullYear();
        let month = currentDate.getMonth();
        currentYearMonthEl.textContent = `${year}年 ${month + 1}月`;
    
        // 曜日の配列
        const weekdays = ['日', '月', '火', '水', '木', '金', '土'];
    
        // 曜日のヘッダーを追加
        weekdays.forEach((day, index) => {
            const dayCell = document.createElement('div');
            dayCell.textContent = day;
            dayCell.classList.add('day-name'); // 曜日用のクラスを追加
            dayCell.style.cursor = 'default'; // 曜日セルにはカーソルをデフォルトに設定
            if (index === 0) {
                dayCell.classList.add('sunday');
            } else if (index === 6) {
                dayCell.classList.add('saturday');
            }
            calendarEl.appendChild(dayCell);
        });

        // 月の日数を取得
        let daysInMonth = new Date(year, month + 1, 0).getDate();

        // 1日の曜日を取得
        let firstDayOfWeek = new Date(year, month, 1).getDay();

        // 前月の空白セルを追加
        for (let i = 0; i < firstDayOfWeek; i++) {
            calendarEl.appendChild(document.createElement('div'));
        }

        // 日付セルを追加
        for (let i = 1; i <= daysInMonth; i++) {
            let cell = document.createElement('div');
            cell.textContent = i;
            let fullDate = `${year}-${month + 1}-${i}`;
        
            // 日記が存在する日付の場合は特別なクラスを適用
            if (diaryDates.includes(fullDate)) {
                cell.classList.add('diary-exists');
            }
        
            cell.addEventListener('click', function() {
                location.href = `/diary/check_entry/?date=${fullDate}`;
            });
            
            calendarEl.appendChild(cell);
        }
    }

    document.getElementById('prev-month').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById('next-month').addEventListener('click', function() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar();
    });

    renderCalendar(); // カレンダーの初期表示
});
