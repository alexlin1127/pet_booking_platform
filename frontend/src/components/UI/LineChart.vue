<script setup>
import { Line } from 'vue-chartjs'
import { Chart, registerables } from 'chart.js'
import { computed } from 'vue';

Chart.register(...registerables)

const props = defineProps({
  chartData: {
    type: Array,
    default: () => []
  },
  label: String
})

const labels = computed(() => Array.isArray(props.chartData) ? props.chartData.map(item => item.date) : [])
const data = computed(() => Array.isArray(props.chartData) ? props.chartData.map(item => item.count) : [])

const chartConfig = computed(() => ({
  labels: labels.value,
  datasets: [
    {
      label: props.label,
      data: data.value,
      borderColor: 'rgba(75,192,192,1)',
      backgroundColor: 'rgba(75,192,192,0.2)',
      fill: true,
      tension: 0.4
    }
  ]
}))
</script>

<template>
  <div class="chart-wrapper">
    <Line
      :data="chartConfig"
      :options="{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: true },
          title: {
            display: true,
            text: '人數'
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: '人數'
            },
            min: 0,
            max: 10,
            ticks: {
              stepSize: 1,
              callback: function(value) {
                return Number.isInteger(value) ? value : null;
              }
            }
          }
        }
      }"
    />
  </div>
</template>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}
</style>