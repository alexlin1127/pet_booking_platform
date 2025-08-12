<template>
  <!-- 表單頁 -->
  <section
    v-if="mode === 'form'"
    class="storeappointment-container storeappointment-page"
  >
    <h1 class="storeappointment-title">新增預約</h1>

    <!-- tabs -->
    <div class="storeappointment-tab-wrap">
      <button
        :class="[
          'storeappointment-tab',
          form.service === 'grooming' && 'storeappointment-tab-active',
        ]"
        @click="switchService('grooming')"
      >
        美容
      </button>
      <button
        :class="[
          'storeappointment-tab',
          form.service === 'lodging' && 'storeappointment-tab-active',
        ]"
        @click="switchService('lodging')"
      >
        住宿
      </button>
    </div>

    <!-- 卡片內容 -->
    <div class="sa-card">
      <div class="sa-card-inner space-y-6">
        <!-- 共用欄位 -->
        <div class="grid md:grid-cols-2 gap-5">
          <div>
            <label class="storeappointment-label">顧客姓名</label>
            <input
              class="storeappointment-input"
              v-model="form.customerName"
              placeholder="請輸入完整姓名"
            />
          </div>
          <div>
            <label class="storeappointment-label">顧客電話（手機）</label>
            <input
              class="storeappointment-input"
              v-model="form.phone"
              placeholder="請輸入電話"
            />
          </div>
          <div>
            <label class="storeappointment-label">毛孩姓名</label>
            <input
              class="storeappointment-input"
              v-model="form.petName"
              placeholder="請輸入毛孩姓名"
            />
          </div>
          <div>
            <label class="storeappointment-label">毛孩類別</label>
            <div class="flex items-center gap-6 pt-2">
              <label class="inline-flex items-center gap-2"
                ><input
                  type="radio"
                  class="storeappointment-radio"
                  value="狗"
                  v-model="form.petType"
                />寵物狗</label
              >
              <label class="inline-flex items-center gap-2"
                ><input
                  type="radio"
                  class="storeappointment-radio"
                  value="貓"
                  v-model="form.petType"
                />寵物貓</label
              >
            </div>
          </div>
        </div>

        <!-- 美容專屬 -->
        <template v-if="form.service === 'grooming'">
          <div class="grid md:grid-cols-2 gap-5">
            <div>
              <label class="storeappointment-label">毛孩種類</label>
              <select class="storeappointment-select" v-model="form.breed">
                <option value="">請選擇毛孩種類</option>
                <option>柴犬</option>
                <option>米克斯</option>
                <option>博美</option>
                <option>貓-短毛</option>
              </select>
            </div>
            <div>
              <label class="storeappointment-label">選擇服務項目</label>
              <select
                class="storeappointment-select"
                v-model="form.groomingService"
              >
                <option value="">請選擇美容項目</option>
                <option>洗澡清潔、手部基礎</option>
                <option>洗澡清潔 + 剪毛造型</option>
              </select>
            </div>
          </div>

          <!-- 時間選擇 -->
          <div>
            <h3 class="block-title text-center">選擇預約時間</h3>
            <div class="timepicker-details">
              <div class="timepicker-summary">
                <span class="font-bold"
                  >{{ calendar.year }}年{{ calendar.month + 1 }}月</span
                >
                <div class="flex gap-3">
                  <button
                    class="storeappointment-tab px-3 w-auto"
                    @click="prevMonth"
                  >
                    ‹
                  </button>
                  <button
                    class="storeappointment-tab px-3 w-auto"
                    @click="nextMonth"
                  >
                    ›
                  </button>
                </div>
              </div>
              <div class="timepicker-calendar">
                <div class="calendar-head">
                  <div class="calendar-title text-gray-600">
                    一 二 三 四 五 六 日
                  </div>
                </div>
                <div class="calendar-grid">
                  <template v-for="(cell, i) in calendarCells" :key="i">
                    <div
                      :class="[
                        'calendar-cell',
                        cell.muted && 'muted',
                        isSameDate(cell.date, form.date) && 'active',
                      ]"
                      @click="selectDate(cell)"
                    >
                      {{ cell.date.getDate() }}
                    </div>
                  </template>
                </div>

                <div class="time-period-row">
                  <button
                    :class="[
                      'time-period',
                      period === 'am' && 'time-period-active',
                    ]"
                    @click="period = 'am'"
                  >
                    上午
                  </button>
                  <button
                    :class="[
                      'time-period',
                      period === 'pm' && 'time-period-active',
                    ]"
                    @click="period = 'pm'"
                  >
                    下午
                  </button>
                </div>

                <div class="time-grid">
                  <button
                    v-for="t in shownSlots"
                    :key="t.time"
                    :class="[
                      'time-slot',
                      t.disabled && 'disabled',
                      form.time === t.time && 'active',
                    ]"
                    :disabled="t.disabled"
                    @click="form.time = t.time"
                  >
                    {{ t.label }}
                  </button>
                </div>

                <div class="subtotal">
                  本次美容預估總金額：<span class="font-semibold">{{
                    groomingPrice.toLocaleString()
                  }}</span>
                </div>
              </div>
            </div>

            <div class="mt-5">
              <label class="storeappointment-label">客服備註</label>
              <textarea
                class="storeappointment-textarea"
                v-model="form.memo"
                placeholder="請輸入備註"
              ></textarea>
            </div>
          </div>
        </template>

        <!-- 住宿專屬 -->
        <template v-else>
          <div class="grid md:grid-cols-2 gap-5">
            <div>
              <label class="storeappointment-label">毛孩種類</label>
              <select class="storeappointment-select" v-model="form.breedSize">
                <option value="大型犬">大型犬</option>
                <option value="中型犬">中型犬</option>
                <option value="小型犬">小型犬</option>
              </select>
            </div>
            <div></div>

            <div>
              <label class="storeappointment-label">到店日期</label>
              <input
                type="date"
                class="storeappointment-input"
                v-model="form.startDate"
              />
            </div>
            <div>
              <label class="storeappointment-label">到店時間</label>
              <select class="storeappointment-select" v-model="form.startTime">
                <option>09:30</option>
                <option>10:00</option>
                <option>10:30</option>
                <option>11:00</option>
              </select>
            </div>

            <div>
              <label class="storeappointment-label">離店日期</label>
              <input
                type="date"
                class="storeappointment-input"
                v-model="form.endDate"
              />
            </div>
            <div>
              <label class="storeappointment-label">離店時間</label>
              <select class="storeappointment-select" v-model="form.endTime">
                <option>18:00</option>
                <option>17:30</option>
                <option>17:00</option>
              </select>
            </div>
          </div>

          <div>
            <label class="storeappointment-label">優惠方案</label>
            <div class="sa-card border mt-1">
              <div class="sa-card-inner text-sm leading-7">
                • 每晚 NT$ 1,200<br />
                • 住三晚，總價 NT$ 3,000<br />
                • 住 1 個月，每晚 NT$ 800
              </div>
            </div>
          </div>

          <div>
            <label class="storeappointment-label">備註</label>
            <textarea
              class="storeappointment-textarea"
              v-model="form.memo"
              placeholder="無"
            ></textarea>
          </div>

          <div class="subtotal">
            本次住宿預估總金額：<span class="font-semibold">{{
              lodgingPrice.toLocaleString()
            }}</span>
          </div>
        </template>

        <!-- 動作列 -->
        <div class="btn-row">
          <button class="btn-ghost" @click="resetForm">取消預約</button>
          <button class="btn-primary" @click="submitForm">送出預約</button>
        </div>
      </div>
    </div>
  </section>

  <!-- 完成頁（美容 & 住宿 通用） -->
  <section v-else class="storeappointment-container">
    <div class="success-wrap">
      <div class="success-icon">✓</div>
      <div class="success-title">完成預約</div>

      <div class="success-card">
        <div class="success-body">
          <div class="success-row">
            <div class="success-label">顧客</div>
            <div class="success-value">
              {{ summary.customerName || "王小明" }}
            </div>
          </div>

          <template v-if="summary.type === 'lodging'">
            <div class="success-row">
              <div class="success-label">到店日期</div>
              <div class="success-value">
                {{ summary.startDate }}（{{ weekday(summary.startDate) }}）
              </div>
            </div>
            <div class="success-row">
              <div class="success-label">到店時間</div>
              <div class="success-value">{{ summary.startTime }}</div>
            </div>
            <div class="success-row">
              <div class="success-label">離店日期</div>
              <div class="success-value">
                {{ summary.endDate }}（{{ weekday(summary.endDate) }}）
              </div>
            </div>
            <div class="success-row">
              <div class="success-label">離店時間</div>
              <div class="success-value">{{ summary.endTime }}</div>
            </div>
            <div class="success-row">
              <div class="success-label">預約天數</div>
              <div class="success-value">{{ summary.days }}天</div>
            </div>
            <div class="success-row">
              <div class="success-label">預約房間</div>
              <div class="success-value">{{ summary.room }}</div>
            </div>
          </template>

          <template v-else>
            <div class="success-row">
              <div class="success-label">預約日期</div>
              <div class="success-value">
                {{ summary.date }}（{{ weekday(summary.date) }}）
              </div>
            </div>
            <div class="success-row">
              <div class="success-label">預約時間</div>
              <div class="success-value">
                {{ summary.timePeriod }} {{ summary.time }}
              </div>
            </div>
            <div class="success-row">
              <div class="success-label">服務項目</div>
              <div class="success-value">洗澡清潔 + 剪毛造型</div>
            </div>
          </template>
        </div>
      </div>

      <div class="contact-card">
        <div class="contact-body">
          <div class="success-label mb-1">連絡電話</div>
          <div class="contact-phone">03-81234567</div>
        </div>
      </div>

      <div class="back-row">
        <button class="btn-back" @click="backToForm">返回</button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data() {
    const today = new Date();
    return {
      mode: "form",
      period: "am",
      /* 表單資料 */
      form: {
        service: "grooming", // 'grooming' | 'lodging'
        customerName: "",
        phone: "",
        petName: "",
        petType: "狗",

        // 美容
        breed: "",
        groomingService: "",
        date: null, // Date 物件
        time: "",

        // 住宿
        breedSize: "大型犬",
        startDate: "",
        startTime: "09:30",
        endDate: "",
        endTime: "18:00",

        memo: "",
      },

      // 簡易月曆
      calendar: { year: today.getFullYear(), month: today.getMonth() },

      // 完成摘要
      summary: {},
    };
  },

  computed: {
    calendarFirstDay() {
      return new Date(this.calendar.year, this.calendar.month, 1);
    },
    calendarCells() {
      const first = this.calendarFirstDay;
      const startWeekIndex = (first.getDay() + 6) % 7; // 讓週一=0
      const daysInMonth = new Date(
        this.calendar.year,
        this.calendar.month + 1,
        0
      ).getDate();

      const cells = [];
      // 前置空白（上一月）
      for (let i = 0; i < startWeekIndex; i++) {
        const d = new Date(
          this.calendar.year,
          this.calendar.month,
          -(startWeekIndex - 1 - i)
        );
        cells.push({ date: d, muted: true });
      }
      // 本月
      for (let d = 1; d <= daysInMonth; d++) {
        cells.push({
          date: new Date(this.calendar.year, this.calendar.month, d),
          muted: false,
        });
      }
      // 補滿 42 格
      while (cells.length < 42) {
        const last = cells[cells.length - 1].date;
        const d = new Date(
          last.getFullYear(),
          last.getMonth(),
          last.getDate() + 1
        );
        cells.push({ date: d, muted: true });
      }
      return cells;
    },

    allSlots() {
      // 以你的圖排：上午 09:00/09:15/09:30(停用)/10:45/11:00/11:15/11:30/11:45/12:00
      return [
        { time: "09:00", label: "09:00", period: "am" },
        { time: "09:15", label: "09:15", period: "am" },
        { time: "09:30", label: "09:30", period: "am", disabled: true },
        { time: "10:45", label: "10:45", period: "am" },
        { time: "11:00", label: "11:00", period: "am" },
        { time: "11:15", label: "11:15", period: "am" },
        { time: "11:30", label: "11:30", period: "am" },
        { time: "11:45", label: "11:45", period: "am" },
        { time: "12:00", label: "12:00", period: "am" },
        // 下午可延伸
        { time: "13:30", label: "13:30", period: "pm" },
        { time: "13:45", label: "13:45", period: "pm" },
        { time: "14:00", label: "14:00", period: "pm" },
        { time: "14:15", label: "14:15", period: "pm" },
        { time: "14:30", label: "14:30", period: "pm" },
        { time: "14:45", label: "14:45", period: "pm" },
        { time: "15:00", label: "15:00", period: "pm" },
        { time: "15:15", label: "15:15", period: "pm" },
        { time: "15:30", label: "15:30", period: "pm" },
      ];
    },
    shownSlots() {
      return this.allSlots.filter((s) => s.period === this.period);
    },

    groomingPrice() {
      // Demo：固定顯示 1,200
      return 1200;
    },
    lodgingPrice() {
      // Demo：固定顯示 1,200
      return 1200;
    },
  },

  methods: {
    switchService(s) {
      this.form.service = s;
    },
    prevMonth() {
      if (this.calendar.month === 0) {
        this.calendar.year--;
        this.calendar.month = 11;
      } else this.calendar.month--;
    },
    nextMonth() {
      if (this.calendar.month === 11) {
        this.calendar.year++;
        this.calendar.month = 0;
      } else this.calendar.month++;
    },

    isSameDate(a, b) {
      if (!a || !b) return false;
      const d = b instanceof Date ? b : new Date(b);
      return (
        a.getFullYear() === d.getFullYear() &&
        a.getMonth() === d.getMonth() &&
        a.getDate() === d.getDate()
      );
    },
    selectDate(cell) {
      if (cell) this.form.date = cell.date;
    },

    resetForm() {
      this.mode = "form";
      this.form.time = "";
      this.form.memo = "";
    },

    weekday(yyyyMMdd) {
      // yyyy-mm-dd
      const dt = new Date(yyyyMMdd || this.formatDate(this.form.date));
      return ["週一", "週二", "週三", "週四", "週五", "週六", "週日"][
        (dt.getDay() + 6) % 7
      ];
    },
    formatDate(d) {
      if (!(d instanceof Date)) return d || "";
      const y = d.getFullYear(),
        m = String(d.getMonth() + 1).padStart(2, "0"),
        day = String(d.getDate()).padStart(2, "0");
      return `${y}/${m}/${day}`;
    },

    submitForm() {
      if (this.form.service === "lodging") {
        this.summary = {
          type: "lodging",
          customerName: this.form.customerName,
          startDate: this.form.startDate.replaceAll("-", "/"),
          startTime: this.form.startTime,
          endDate: this.form.endDate.replaceAll("-", "/"),
          endTime: this.form.endTime,
          days: 1,
          room: this.form.breedSize,
        };
      } else {
        this.summary = {
          type: "grooming",
          customerName: this.form.customerName,
          date: this.formatDate(this.form.date),
          time: this.form.time || "11:30 – 12:00",
          timePeriod: this.period === "am" ? "上午" : "下午",
        };
      }
      this.mode = "done";
    },

    backToForm() {
      this.mode = "form";
    },
  },
};
</script>

<!-- 有設定 alias「@」指到 src 的話可直接用這行；否則換成相對路徑 -->
<style
  src="../../styles/pages/Stores/storeappointment/storeappointment.css"
></style>
