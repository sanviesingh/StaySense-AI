function toggleTheme(){
    document.body.classList.toggle("dark");

    const button = document.querySelector(".theme-toggle");
    if (button) {
        button.textContent = document.body.classList.contains("dark")
            ? "☀️ Light Mode"
            : "🌙 Dark Mode";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const button = document.querySelector(".theme-toggle");
    if (button) {
        button.addEventListener("click", toggleTheme);
    }
});

// Dashboard animations
function initProgressCircles(){
    const circles = document.querySelectorAll('.progress-circle');
    circles.forEach(el => {
        const percent = parseInt(el.dataset.percent || '0', 10);
        const size = 90;
        const stroke = 10;
        const radius = (size - stroke) / 2;
        const circumference = 2 * Math.PI * radius;

        const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
        svg.setAttribute('width', size);
        svg.setAttribute('height', size);
        const g = document.createElementNS(svg.namespaceURI, 'g');
        g.setAttribute('transform', `translate(${size/2}, ${size/2})`);

        const bg = document.createElementNS(svg.namespaceURI, 'circle');
        bg.setAttribute('r', radius);
        bg.setAttribute('fill', 'none');
        bg.setAttribute('stroke', 'rgba(255,255,255,0.18)');
        bg.setAttribute('stroke-width', stroke);

        const fg = document.createElementNS(svg.namespaceURI, 'circle');
        fg.setAttribute('r', radius);
        fg.setAttribute('fill', 'none');
        fg.setAttribute('stroke', '#fff');
        fg.setAttribute('stroke-width', stroke);
        fg.setAttribute('stroke-linecap', 'round');
        fg.setAttribute('transform', 'rotate(-90)');
        fg.style.strokeDasharray = circumference;
        fg.style.strokeDashoffset = circumference;

        g.appendChild(bg);
        g.appendChild(fg);
        svg.appendChild(g);
        el.appendChild(svg);

        // animate
        setTimeout(()=>{
            const offset = circumference * (1 - percent/100);
            fg.style.transition = 'stroke-dashoffset 1s ease-out';
            fg.style.strokeDashoffset = offset;
        }, 200);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initProgressCircles();
});

// Initialize sentiment chart using Chart.js (loaded from CDN in template)
function initSentimentChart(){
    const canvas = document.getElementById('sentimentChart');
    if (!canvas) return;
    const positive = parseInt(canvas.dataset.positive || '0',10);
    const negative = parseInt(canvas.dataset.negative || '0',10);
    const neutral = parseInt(canvas.dataset.neutral || '0',10);

    if (typeof Chart === 'undefined') return;

    new Chart(canvas.getContext('2d'), {
        type: 'doughnut',
        data: {
            labels: ['Positive','Negative','Neutral'],
            datasets: [{
                data: [positive, negative, neutral],
                backgroundColor: ['#10b981','#ef4444','#f59e0b'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {legend:{position:'bottom'}}
        }
    });
}

function initThemeChart(){
    const canvas = document.getElementById('themesBarChart');
    if (!canvas) return;
    const data = canvas.dataset.themes ? JSON.parse(canvas.dataset.themes) : {};

    if (typeof Chart === 'undefined') return;

    const labels = Object.keys(data);
    const values = Object.values(data);

    new Chart(canvas.getContext('2d'), {
        type: 'bar',
        data: {
            labels,
            datasets: [{
                label: 'Theme Count',
                data: values,
                backgroundColor: labels.map(label => {
                    if (label === 'Food') return '#65a30d';
                    if (label === 'Cleanliness') return '#22c55e';
                    if (label === 'Location') return '#0ea5e9';
                    if (label === 'Host') return '#8b5cf6';
                    return '#94a3b8';
                }),
                borderRadius: 8,
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { grid: { display:false }, ticks: { color:'#0f172a' } },
                y: { grid: { color:'rgba(15,23,42,0.08)' }, beginAtZero:true, ticks: { color:'#0f172a' } }
            },
            plugins: {legend:{display:false}}
        }
    });
}

function initCalendar(){
    const container = document.getElementById('calendarWidget');
    if (!container) return;

    const days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
    container.innerHTML = '';

    for (let day of days) {
        const header = document.createElement('div');
        header.className = 'day-header';
        header.textContent = day;
        container.appendChild(header);
    }

    const totalDays = 30;
    const today = new Date().getDate();
    for (let i = 1; i <= totalDays; i++) {
        const dayBlock = document.createElement('div');
        dayBlock.textContent = i;
        if (i === today) {
            dayBlock.style.background = '#16a34a';
            dayBlock.style.color = 'white';
            dayBlock.style.fontWeight = '700';
        }
        if ([4, 10, 18, 23].includes(i)) {
            const note = document.createElement('div');
            note.className = 'event-label';
            note.textContent = 'Review event';
            dayBlock.appendChild(note);
        }
        container.appendChild(dayBlock);
    }
}

document.addEventListener('DOMContentLoaded', ()=>{
    initSentimentChart();
    initThemeChart();
    initCalendar();
});