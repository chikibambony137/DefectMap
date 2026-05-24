<template>
  <div class="stats-page q-pa-lg">

    <!-- Заголовок -->
    <div class="row items-center q-mb-lg">
      <div>
        <div class="stats-title">Аналитика</div>
        <div class="stats-subtitle">Сводная статистика по приборам и дефектам</div>
      </div>
      <q-space />
      <div class="row q-gutter-sm">
        <q-btn flat
               round
               icon="refresh"
               color="grey-6"
               @click="loadAll"
               :loading="loading" />
        <q-btn flat
               round
               icon="picture_as_pdf"
               color="negative"
               @click="exportPdf"
               :loading="exporting">
          <q-tooltip>Экспорт в PDF</q-tooltip>
        </q-btn>
      </div>
    </div>

    <!-- KPI карточки -->
    <div class="row q-gutter-md q-mb-lg">
      <div class="kpi-card col" v-for="kpi in kpiCards" :key="kpi.label">
        <div class="kpi-icon" :style="{ background: kpi.bg }">
          <q-icon :name="kpi.icon" :color="kpi.color" size="22px" />
        </div>
        <div class="kpi-value">{{ kpi.value }}</div>
        <div class="kpi-label">{{ kpi.label }}</div>
      </div>
    </div>

    <!-- Графики: строка 1 -->
    <div class="row q-gutter-md q-mb-md">

      <!-- Дефекты по статусу -->
      <q-card flat bordered class="chart-card col">
        <q-card-section>
          <div class="chart-title">Дефекты по статусу</div>
        </q-card-section>
        <q-card-section class="flex flex-center">
          <div style="width: 260px; height: 260px" v-if="defectsByStatus.labels.length">
            <Doughnut :data="defectsByStatus" :options="doughnutOptions" />
          </div>
          <div v-else class="text-grey-5 text-caption">Нет данных</div>
        </q-card-section>
      </q-card>

      <!-- Дефекты по критичности -->
      <q-card flat bordered class="chart-card col">
        <q-card-section>
          <div class="chart-title">Дефекты по критичности</div>
        </q-card-section>
        <q-card-section class="flex flex-center">
          <div style="width: 260px; height: 260px" v-if="defectsByCriticality.labels.length">
            <Doughnut :data="defectsByCriticality" :options="doughnutOptions" />
          </div>
          <div v-else class="text-grey-5 text-caption">Нет данных</div>
        </q-card-section>
      </q-card>

      <!-- Приборы по статусу -->
      <q-card flat bordered class="chart-card col">
        <q-card-section>
          <div class="chart-title">Приборы по статусу</div>
        </q-card-section>
        <q-card-section class="flex flex-center">
          <div style="width: 260px; height: 260px" v-if="equipmentByStatus.labels.length">
            <Doughnut :data="equipmentByStatus" :options="doughnutOptions" />
          </div>
          <div v-else class="text-grey-5 text-caption">Нет данных</div>
        </q-card-section>
      </q-card>

    </div>

    <!-- Графики: строка 2 -->
    <div class="row q-gutter-md q-mb-md">

      <!-- Динамика дефектов по месяцам -->
      <q-card flat bordered class="chart-card col-8">
        <q-card-section>
          <div class="chart-title">Динамика дефектов по месяцам</div>
        </q-card-section>
        <q-card-section>
          <div style="height: 220px" v-if="defectsByMonth.labels.length">
            <Line :data="defectsByMonth" :options="lineOptions" />
          </div>
          <div v-else class="text-grey-5 text-caption flex flex-center" style="height:220px">Нет данных</div>
        </q-card-section>
      </q-card>

      <!-- Дефекты по типу -->
      <q-card flat bordered class="chart-card col">
        <q-card-section>
          <div class="chart-title">По типу дефекта</div>
        </q-card-section>
        <q-card-section>
          <div style="height: 220px" v-if="defectsByType.labels.length">
            <Bar :data="defectsByType" :options="barHorizOptions" />
          </div>
          <div v-else class="text-grey-5 text-caption flex flex-center" style="height:220px">Нет данных</div>
        </q-card-section>
      </q-card>

    </div>

    <!-- Таблица: топ приборов по дефектам -->
    <q-card flat bordered>
      <q-card-section>
        <div class="chart-title">Топ приборов по количеству дефектов</div>
      </q-card-section>
      <q-card-section>
        <q-table
          flat
          dense
          :rows="topEquipment"
          :columns="topColumns"
          :loading="loading"
          row-key="id"
          :rows-per-page-options="[10]"
          hide-bottom
        >
          <template #body-cell-open_defects_count="props">
            <q-td :props="props">
              <q-badge
                :color="props.row.open_defects_count > 0 ? 'negative' : 'positive'"
                :label="props.row.open_defects_count"
              />
            </q-td>
          </template>
          <template #body-cell-defects_count="props">
            <q-td :props="props">
              <div class="row items-center" style="gap: 8px">
                <div
                  class="defect-bar"
                  :style="{ width: barWidth(props.row.defects_count) }"
                />
                {{ props.row.defects_count }}
              </div>
            </q-td>
          </template>
        </q-table>
      </q-card-section>
    </q-card>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { Doughnut, Line, Bar } from 'vue-chartjs';
import {
  Chart as ChartJS,
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement,
  BarElement, Filler
} from 'chart.js';

import { apiRequest } from 'src/stores/api';
import { useEquipmentStatusStore } from 'src/stores/useEquipmentStatusStore';
import { useDefectStatusStore } from 'src/stores/useDefectStatusStore';
import { useDefectCriticalitiesStore } from 'src/stores/useDefectCriticalitiesStore';
import { useDefectTypeStore } from 'src/stores/useDefectTypeStore';

ChartJS.register(
  ArcElement, Tooltip, Legend,
  CategoryScale, LinearScale,
  PointElement, LineElement,
  BarElement, Filler
);

const statusStore = useEquipmentStatusStore();
const defectStatusStore = useDefectStatusStore();
const criticalityStore = useDefectCriticalitiesStore();
const defectTypeStore = useDefectTypeStore();

const loading = ref(false);
const exporting = ref(false);
const defects = ref([]);
const equipmentWithStats = ref([]);

// ─── Экспорт PDF ─────────────────────────────────────────────
async function loadFont(doc) {
  const url = 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/fonts/Roboto/Roboto-Regular.ttf';
  const boldUrl = 'https://cdnjs.cloudflare.com/ajax/libs/pdfmake/0.2.7/fonts/Roboto/Roboto-Medium.ttf';

  const toBase64 = async(fontUrl) => {
    const res = await fetch(fontUrl);
    const buf = await res.arrayBuffer();
    const bytes = new Uint8Array(buf);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) binary += String.fromCharCode(bytes[i]);
    return btoa(binary);
  };

  const [regular, bold] = await Promise.all([toBase64(url), toBase64(boldUrl)]);
  doc.addFileToVFS('Roboto-Regular.ttf', regular);
  doc.addFileToVFS('Roboto-Bold.ttf', bold);
  doc.addFont('Roboto-Regular.ttf', 'Roboto', 'normal');
  doc.addFont('Roboto-Bold.ttf', 'Roboto', 'bold');
}

async function exportPdf() {
  exporting.value = true;
  try {
    const doc = new jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' });
    await loadFont(doc);

    const pageW = doc.internal.pageSize.getWidth();
    const now = new Date().toLocaleString('ru');

    // ── Заголовок ──
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(18);
    doc.text('Аналитика: приборы и дефекты', pageW / 2, 18, { align: 'center' });
    doc.setFont('Roboto', 'normal');
    doc.setFontSize(9);
    doc.setTextColor(140);
    doc.text(`Сформировано: ${now}`, pageW / 2, 24, { align: 'center' });
    doc.setTextColor(0);

    const tableDefaults = {
      styles: { fontSize: 10, cellPadding: 3, font: 'Roboto' },
      headStyles: { fillColor: [74, 144, 217], textColor: 255, fontStyle: 'bold', font: 'Roboto' },
      alternateRowStyles: { fillColor: [245, 248, 255] }
    };

    // ── KPI таблица ──
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(12);
    doc.text('Ключевые показатели', 14, 34);

    autoTable(doc, {
      ...tableDefaults,
      startY: 38,
      head: [['Показатель', 'Значение']],
      body: kpiCards.value.map(k => [k.label, String(k.value)]),
      columnStyles: { 1: { halign: 'center', fontStyle: 'bold' } }
    });

    // ── Дефекты по статусу ──
    let y = doc.lastAutoTable.finalY + 10;
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(12);
    doc.text('Дефекты по статусу', 14, y);
    autoTable(doc, {
      ...tableDefaults,
      startY: y + 4,
      head: [['Статус', 'Количество']],
      body: defectsByStatus.value.labels.map((l, i) => [l, defectsByStatus.value.datasets[0].data[i]]),
      columnStyles: { 1: { halign: 'center' } }
    });

    // ── Дефекты по критичности ──
    y = doc.lastAutoTable.finalY + 10;
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(12);
    doc.text('Дефекты по критичности', 14, y);
    autoTable(doc, {
      ...tableDefaults,
      startY: y + 4,
      head: [['Критичность', 'Количество']],
      body: defectsByCriticality.value.labels.map((l, i) => [l, defectsByCriticality.value.datasets[0].data[i]]),
      columnStyles: { 1: { halign: 'center' } }
    });

    // ── Приборы по статусу ──
    y = doc.lastAutoTable.finalY + 10;
    if (y > 240) { doc.addPage(); y = 14; }
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(12);
    doc.text('Приборы по статусу', 14, y);
    autoTable(doc, {
      ...tableDefaults,
      startY: y + 4,
      head: [['Статус', 'Количество']],
      body: equipmentByStatus.value.labels.map((l, i) => [l, equipmentByStatus.value.datasets[0].data[i]]),
      columnStyles: { 1: { halign: 'center' } }
    });

    // ── Топ приборов (новая страница) ──
    doc.addPage();
    doc.setFont('Roboto', 'bold');
    doc.setFontSize(12);
    doc.text('Топ приборов по дефектам', 14, 14);
    autoTable(doc, {
      ...tableDefaults,
      startY: 18,
      head: [['Серийный номер', 'Модель', 'Адрес', 'Всего дефектов', 'Открытых']],
      body: topEquipment.value.map(e => [
        e.serial_number,
        e.model,
        e.location_address,
        e.defects_count,
        e.open_defects_count
      ]),
      styles: { fontSize: 9, cellPadding: 2.5, font: 'Roboto' },
      columnStyles: {
        3: { halign: 'center' },
        4: { halign: 'center' }
      }
    });

    // ── Нумерация страниц ──
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
      doc.setPage(i);
      doc.setFont('Roboto', 'normal');
      doc.setFontSize(8);
      doc.setTextColor(160);
      doc.text(`Страница ${i} из ${pageCount}`, pageW / 2, doc.internal.pageSize.getHeight() - 6, { align: 'center' });
    }

    doc.save(`defectmap-stats-${new Date().toISOString().slice(0, 10)}.pdf`);
  } finally {
    exporting.value = false;
  }
}

// ─── Загрузка ────────────────────────────────────────────────
async function loadAll() {
  loading.value = true;
  try {
    const [defectsRes, equipmentRes] = await Promise.all([
      apiRequest('/defects/?skip=0&limit=1000'),
      apiRequest('/equipment/with-stats')
    ]);
    if (defectsRes) defects.value = await defectsRes.json();
    if (equipmentRes) equipmentWithStats.value = await equipmentRes.json();

    if (!statusStore.statuses.length) await statusStore.fetchEquipmentStatuses();
    if (!defectStatusStore.statuses.length) await defectStatusStore.fetchDefectStatuses();
    if (!criticalityStore.defectCriticalities.length) await criticalityStore.fetchDefectCriticalities();
    if (!defectTypeStore.defectTypes.length) await defectTypeStore.fetchDefectTypes();
  } finally {
    loading.value = false;
  }
}

onMounted(loadAll);

// ─── KPI карточки ────────────────────────────────────────────
const kpiCards = computed(() => {
  const totalEquipment = equipmentWithStats.value.length;
  const activeStatusId = statusStore.statuses.find(s => s.name === 'Активен')?.id;
  const activeEquipment = equipmentWithStats.value.filter(e => e.status_id === activeStatusId).length;

  const totalDefects = defects.value.length;
  const openStatusId = defectStatusStore.statuses.find(s => s.name === 'Открыт')?.id;
  const openDefects = defects.value.filter(d => d.status_id === openStatusId).length;

  const resolved = defects.value.filter(d => d.resolved_at);
  const avgDays = resolved.length
    ? Math.round(
      resolved.reduce((acc, d) => {
        const diff = new Date(d.resolved_at) - new Date(d.created_at);
        return acc + diff / 86400000;
      }, 0) / resolved.length
    )
    : null;

  return [
    { label: 'Всего приборов',    value: totalEquipment,  icon: 'devices',       color: 'blue-7',     bg: '#e3f0ff' },
    { label: 'Активных приборов', value: activeEquipment, icon: 'check_circle',  color: 'positive',   bg: '#e6f9ef' },
    { label: 'Всего дефектов',    value: totalDefects,    icon: 'bug_report',    color: 'orange-8',   bg: '#fff4e3' },
    { label: 'Открытых дефектов', value: openDefects,     icon: 'warning',       color: 'negative',   bg: '#fde8e8' },
    { label: 'Среднее время устранения (дней)', value: avgDays ?? '—', icon: 'schedule', color: 'purple-6', bg: '#f3eeff' }
  ];
});

// ─── Палитры ─────────────────────────────────────────────────
const PALETTE = ['#4A90D9', '#50C878', '#F5A623', '#E74C3C', '#9B59B6', '#1ABC9C', '#E67E22'];

// ─── Дефекты по статусу ──────────────────────────────────────
const defectsByStatus = computed(() => {
  const map = {};
  for (const d of defects.value) {
    const name = defectStatusStore.statuses.find(s => s.id === d.status_id)?.name ?? `Статус ${d.status_id}`;
    map[name] = (map[name] ?? 0) + 1;
  }
  return {
    labels: Object.keys(map),
    datasets: [{ data: Object.values(map), backgroundColor: PALETTE, borderWidth: 0 }]
  };
});

// ─── Дефекты по критичности ──────────────────────────────────
const defectsByCriticality = computed(() => {
  const map = {};
  for (const d of defects.value) {
    const name = criticalityStore.defectCriticalities.find(c => c.id === d.criticality_id)?.name ?? `Критичность ${d.criticality_id}`;
    map[name] = (map[name] ?? 0) + 1;
  }
  const sorted = Object.entries(map).sort((a, b) => {
    const wa = criticalityStore.defectCriticalities.find(c => c.name === a[0])?.weight ?? 0;
    const wb = criticalityStore.defectCriticalities.find(c => c.name === b[0])?.weight ?? 0;
    return wb - wa;
  });
  return {
    labels: sorted.map(([k]) => k),
    datasets: [{ data: sorted.map(([, v]) => v), backgroundColor: ['#E74C3C', '#F5A623', '#50C878', '#4A90D9'], borderWidth: 0 }]
  };
});

// ─── Приборы по статусу ──────────────────────────────────────
const equipmentByStatus = computed(() => {
  const map = {};
  for (const e of equipmentWithStats.value) {
    const name = statusStore.statuses.find(s => s.id === e.status_id)?.name ?? `Статус ${e.status_id}`;
    map[name] = (map[name] ?? 0) + 1;
  }
  return {
    labels: Object.keys(map),
    datasets: [{ data: Object.values(map), backgroundColor: PALETTE, borderWidth: 0 }]
  };
});

// ─── Динамика дефектов по месяцам ───────────────────────────
const defectsByMonth = computed(() => {
  const map = {};
  for (const d of defects.value) {
    const date = new Date(d.created_at);
    const key = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
    map[key] = (map[key] ?? 0) + 1;
  }
  const sorted = Object.keys(map).sort();
  return {
    labels: sorted.map(k => {
      const [y, m] = k.split('-');
      return new Date(y, m - 1).toLocaleString('ru', { month: 'short', year: '2-digit' });
    }),
    datasets: [{
      label: 'Дефекты',
      data: sorted.map(k => map[k]),
      borderColor: '#4A90D9',
      backgroundColor: 'rgba(74,144,217,0.12)',
      fill: true,
      tension: 0.4,
      pointRadius: 4,
      pointBackgroundColor: '#4A90D9'
    }]
  };
});

// ─── Дефекты по типу ─────────────────────────────────────────
const defectsByType = computed(() => {
  const map = {};
  for (const d of defects.value) {
    const name = defectTypeStore.defectTypes.find(t => t.id === d.defect_type_id)?.name ?? `Тип ${d.defect_type_id}`;
    map[name] = (map[name] ?? 0) + 1;
  }
  const sorted = Object.entries(map).sort((a, b) => b[1] - a[1]).slice(0, 7);
  return {
    labels: sorted.map(([k]) => k),
    datasets: [{
      data: sorted.map(([, v]) => v),
      backgroundColor: PALETTE,
      borderWidth: 0,
      borderRadius: 4
    }]
  };
});

// ─── Топ приборов ────────────────────────────────────────────
const topEquipment = computed(() =>
  [...equipmentWithStats.value]
    .filter(e => e.defects_count > 0)
    .sort((a, b) => b.defects_count - a.defects_count)
    .slice(0, 10)
);

const maxDefects = computed(() => Math.max(...topEquipment.value.map(e => e.defects_count), 1));
const barWidth = (count) => `${Math.round((count / maxDefects.value) * 80)}px`;

const topColumns = [
  { name: 'serial_number',      label: 'Серийный номер',      field: 'serial_number',      align: 'left' },
  { name: 'model',              label: 'Модель',              field: 'model',              align: 'left' },
  { name: 'location_address',   label: 'Адрес',               field: 'location_address',   align: 'left' },
  { name: 'defects_count',      label: 'Всего дефектов',      field: 'defects_count',      align: 'left', sortable: true },
  { name: 'open_defects_count', label: 'Открытых дефектов',   field: 'open_defects_count', align: 'center', sortable: true }
];

// ─── Опции графиков ──────────────────────────────────────────
const doughnutOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: { position: 'bottom', labels: { boxWidth: 12, padding: 12, font: { size: 12 } } },
    tooltip: { callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed}` } }
  },
  cutout: '62%'
};

const lineOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { display: false }, ticks: { font: { size: 11 } } },
    y: { grid: { color: '#f0f0f0' }, ticks: { precision: 0, font: { size: 11 } }, beginAtZero: true }
  }
};

const barHorizOptions = {
  responsive: true,
  maintainAspectRatio: false,
  indexAxis: 'y',
  plugins: { legend: { display: false } },
  scales: {
    x: { grid: { color: '#f0f0f0' }, ticks: { precision: 0, font: { size: 11 } }, beginAtZero: true },
    y: { grid: { display: false }, ticks: { font: { size: 11 } } }
  }
};
</script>

<style scoped>
.stats-page {
  max-width: 1400px;
}

.stats-title {
  font-size: 22px;
  font-weight: 700;
  color: #1a1a2e;
  letter-spacing: -0.3px;
}

.stats-subtitle {
  font-size: 13px;
  color: #8a8fa8;
  margin-top: 2px;
}

/* KPI */
.kpi-card {
  background: #fff;
  border: 1px solid #eaedf3;
  border-radius: 12px;
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 140px;
}

.kpi-icon {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4px;
}

.kpi-value {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a2e;
  line-height: 1;
}

.kpi-label {
  font-size: 12px;
  color: #8a8fa8;
  line-height: 1.3;
}

/* Карточки графиков */
.chart-card {
  border-radius: 12px !important;
  border-color: #eaedf3 !important;
}

.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #1a1a2e;
}

/* Мини-бар в таблице */
.defect-bar {
  height: 6px;
  background: #4A90D9;
  border-radius: 3px;
  min-width: 4px;
  transition: width 0.3s;
}
</style>
