<script>
export default {
  name: "PetCosmetic",
  data() {
    const now = new Date();
    return {
      sidebarOpen: true,
      step: "form",

      storeName: "毛寶貝精緻美容沙龍",
      serviceList: ["洗澡", "剪毛", "全方位護理", "染毛"],
      service: "洗澡",
      homeService: "否",
      note: "",

      pets: [
        {
          id: 1,
          name: "小白",
          kind: "狗狗",
          gender: "公",
          breed: "米克斯",
          hairLength: "短毛",
          temper: "溫和",
          age: 3,
          weight: 8.2,
          neuter: "是",
          chip: "是",
          remark: "",
        },
      ],
      selectedPetId: 1,

      showPetModal: false,
      modalPet: {},

      currentYear: now.getFullYear(),
      currentMonth: now.getMonth(),
      selectedDate: new Date(now.getFullYear(), now.getMonth(), now.getDate()),

      half: "AM",
      selectedTime: "11:30",

      baseAmount: 1200,
    };
  },
  computed: {
    weekNames() {
      return ["一", "二", "三", "四", "五", "六", "日"];
    },
    firstDayOfMonth() {
      const date = new Date(this.currentYear, this.currentMonth, 1);
      let w = date.getDay();
      if (w === 0) w = 7;
      return w - 1;
    },
    daysInMonth() {
      return new Date(this.currentYear, this.currentMonth + 1, 0).getDate();
    },
    timeOptions() {
      const make = (start, end) => {
        const out = [];
        let [h, m] = start;
        while (h < end[0] || (h === end[0] && m <= end[1])) {
          const hh = String(h).padStart(2, "0");
          const mm = String(m).padStart(2, "0");
          out.push(`${hh}:${mm}`);
          m += 15;
          if (m >= 60) {
            m = 0;
            h += 1;
          }
        }
        return out;
      };
      return this.half === "AM"
        ? make([9, 0], [12, 0])
        : make([13, 0], [17, 0]);
    },
    finishDateText() {
      const y = this.selectedDate.getFullYear();
      const m = this.selectedDate.getMonth() + 1;
      const d = this.selectedDate.getDate();
      const weekday = ["日", "一", "二", "三", "四", "五", "六"][
        this.selectedDate.getDay()
      ];
      return `${y}/${String(m).padStart(2, "0")}/${String(d).padStart(
        2,
        "0"
      )}（週${weekday}）`;
    },
    finishTimeText() {
      const [hh, mm] = this.selectedTime.split(":").map((n) => +n);
      const start = new Date(0, 0, 0, hh, mm);
      const end = new Date(0, 0, 0, hh, mm + 30);
      const fmt = (dt) =>
        `${String(dt.getHours()).padStart(2, "0")}:${String(
          dt.getMinutes()
        ).padStart(2, "0")}`;
      const ampm = hh < 12 ? "上午" : "下午";
      return `${ampm} ${fmt(start)} – ${fmt(end)}`;
    },
    totalAmount() {
      return this.baseAmount;
    },
  },
  methods: {
    isSelectedDate(d) {
      return (
        this.selectedDate.getFullYear() === this.currentYear &&
        this.selectedDate.getMonth() === this.currentMonth &&
        this.selectedDate.getDate() === d
      );
    },
    selectDate(d) {
      this.selectedDate = new Date(this.currentYear, this.currentMonth, d);
    },
    prevMonth() {
      if (this.currentMonth === 0) {
        this.currentMonth = 11;
        this.currentYear -= 1;
      } else this.currentMonth -= 1;
    },
    nextMonth() {
      if (this.currentMonth === 11) {
        this.currentMonth = 0;
        this.currentYear += 1;
      } else this.currentMonth += 1;
    },
    goConfirm() {
      this.step = "done";
    },
    handlePetClick(p) {
      this.selectedPetId = p.id;
      this.modalPet = JSON.parse(JSON.stringify(p));
      this.showPetModal = true;
    },
    addNewPet() {
      this.modalPet = {
        id: Date.now(),
        name: "",
        kind: "狗狗",
        gender: "",
        breed: "",
        hairLength: "",
        temper: "",
        age: null,
        weight: null,
        neuter: "",
        chip: "",
        remark: "",
      };
      this.showPetModal = true;
    },
    closeModal() {
      this.showPetModal = false;
    },
    savePet() {
      const idx = this.pets.findIndex((x) => x.id === this.modalPet.id);
      if (idx >= 0) this.$set(this.pets, idx, { ...this.modalPet });
      else this.pets.push({ ...this.modalPet });
      this.selectedPetId = this.modalPet.id;
      this.closeModal();
    },
  },
};
</script>

<template>
  <div class="petcosmetic-page pc-main">
    <!-- Main -->
    <main class="pc-content pc-main-content">
      <h1 class="pc-title">預約美容服務</h1>

      <section class="pc-card">
        <!-- ▲ 表單上半區：做成你截圖的樣子 -->
        <form class="pc-form-top" @submit.prevent>
          <!-- 選擇店家 -->
          <div class="pc-form-row">
            <label class="pc-label">選擇店家</label>
            <input class="pc-input pc-input-lg" type="text" placeholder="毛寶貝精緻美容沙龍" v-model="storeName" />
          </div>

          <!-- 請選擇本次美容的毛孩子（點小白會開 Modal） -->
          <div class="pc-form-row">
            <label class="pc-label">請選擇本次美容的毛孩子</label>
            <div class="pc-pill-row">
              <button v-for="p in pets" :key="p.id" type="button" class="pc-pill"
                :class="{ active: selectedPetId === p.id }" @click="handlePetClick(p)">
                {{ p.name }}
              </button>
              <button type="button" class="pc-pill ghost" @click="addNewPet">
                新增
              </button>
            </div>
          </div>

          <!-- 選擇服務項目 -->
          <div class="pc-form-row">
            <label class="pc-label">選擇服務項目</label>
            <div class="pc-pill-row">
              <button v-for="s in serviceList" :key="s" type="button" class="pc-pill" :class="{ active: service === s }"
                @click="service = s">
                {{ s }}
              </button>
            </div>
          </div>

          <!-- 是否到府服務 -->
          <div class="pc-form-row">
            <label class="pc-label">是否到府服務</label>
            <div class="pc-radio-inline">
              <label><input class="pc-radio" type="radio" value="是" v-model="homeService" />
                是</label>
              <label><input class="pc-radio" type="radio" value="否" v-model="homeService" />
                否</label>
            </div>
          </div>
        </form>

        <!-- ▼ 其餘區塊：時間 / 備註 / 按鈕（沿用前版） -->
        <h2 class="pc-section-title mt-10">選擇預約時間</h2>

        <div class="pc-datepicker">
          <div class="pc-cal-head">
            <button class="pc-cal-nav" @click="prevMonth" type="button">
              ‹
            </button>
            <div class="pc-cal-title">
              {{ currentYear }}年{{ currentMonth + 1 }}月
            </div>
            <button class="pc-cal-nav" @click="nextMonth" type="button">
              ›
            </button>
          </div>

          <div class="pc-cal-grid pc-cal-week">
            <div v-for="w in weekNames" :key="w">{{ w }}</div>
          </div>

          <div class="pc-cal-grid pc-cal-days">
            <div v-for="n in firstDayOfMonth" :key="'e' + n" class="pc-cal-empty" />
            <button v-for="d in daysInMonth" :key="d" class="pc-cal-day" :class="{ active: isSelectedDate(d) }"
              @click="selectDate(d)" type="button">
              {{ d }}
            </button>
          </div>
        </div>

        <div class="pc-halfday">
          <button type="button" class="pc-half-btn" :class="{ active: half === 'AM' }" @click="half = 'AM'">
            上午
          </button>
          <button type="button" class="pc-half-btn" :class="{ active: half === 'PM' }" @click="half = 'PM'">
            下午
          </button>
        </div>

        <div class="pc-time-grid">
          <button v-for="t in timeOptions" :key="t" class="pc-slot" :class="{ active: selectedTime === t }"
            @click="selectedTime = t" type="button">
            {{ t }}
          </button>
        </div>

        <div class="mt-6">
          <label class="pc-label">備註</label>
          <textarea class="pc-textarea" placeholder="請輸入您想與設計師說明的情況" v-model="note" />
        </div>

        <div class="pc-total">
          本次美容預估金額：<b>{{ totalAmount.toLocaleString() }}</b>
        </div>

        <button class="pc-confirm-btn" type="button" @click="goConfirm">
          確認預約
        </button>
      </section>

      <!-- 完成預約畫面（保留） -->
      <section v-if="step === 'done'" class="pc-finish-wrap">
        <div class="pc-finish-icon">
          <svg viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="11" stroke="#3bb272" stroke-width="2" />
            <path d="M7 12.5l3.2 3.2L17 9" stroke="#3bb272" stroke-width="2" />
          </svg>
        </div>
        <div class="pc-finish-title">完成預約</div>
        <div class="pc-finish-sub">感謝您的預約！</div>
        <button class="pc-finish-wait-btn" type="button">請等待店家審核</button>

        <div class="pc-finish-info-card">
          <div class="pc-finish-info-row"><span>顧客</span><b>王小明</b></div>
          <div class="pc-finish-info-row">
            <span>預約日期</span><b>{{ finishDateText }}</b>
          </div>
          <div class="pc-finish-info-row">
            <span>預約時間</span><b>{{ finishTimeText }}</b>
          </div>
          <div class="pc-finish-info-row">
            <span>服務項目</span><b>{{ service }}</b>
          </div>
          <div class="pc-finish-info-row">
            <span>聯絡店家</span><b>03-81234567</b>
          </div>
        </div>

        <div class="pc-finish-coupon-card">
          <div class="pc-finish-coupon-label">本次使用註冊優惠</div>
          <div class="pc-finish-coupon-code">sfsd654xv46334</div>
        </div>

        <button class="pc-finish-btn" type="button" @click="step = 'form'">
          返回
        </button>
      </section>
    </main>

    <!-- Modal：小白資料 -->
    <transition name="fade">
      <div v-if="showPetModal" class="pc-modal" @click.self="closeModal">
        <div class="pc-modal-card pc-modal-elev">
          <!-- 頂部標題列 -->
          <div class="pc-modal-header">
            <div class="pc-modal-title">
              毛孩基本資料
              <small v-if="modalPet.name">｜{{ modalPet.name }}</small>
            </div>
            <button class="pc-modal-close" @click="closeModal" aria-label="關閉">
              ×
            </button>
          </div>

          <!-- 內容 -->
          <div class="pc-modal-body">
            <div class="pc-modal-grid">
              <div>
                <label class="pc-label">毛孩別</label>
                <div class="pc-radio-inline">
                  <label><input class="pc-radio" type="radio" value="狗狗" v-model="modalPet.kind" />
                    狗狗</label>
                  <label><input class="pc-radio" type="radio" value="貓貓" v-model="modalPet.kind" />
                    貓貓</label>
                </div>
              </div>

              <div>
                <label class="pc-label">毛孩性別</label>
                <select class="pc-select" v-model="modalPet.gender">
                  <option value="" disabled>請選擇</option>
                  <option>公</option>
                  <option>母</option>
                </select>
              </div>

              <div>
                <label class="pc-label">毛孩名字</label>
                <input class="pc-input" v-model="modalPet.name" placeholder="請輸入毛孩名字" />
              </div>

              <div>
                <label class="pc-label">毛孩品種</label>
                <input class="pc-input" v-model="modalPet.breed" placeholder="請輸入毛孩品種" />
              </div>

              <div>
                <label class="pc-label">毛髮長度</label>
                <select class="pc-select" v-model="modalPet.hairLength">
                  <option value="" disabled>請選擇</option>
                  <option>短毛</option>
                  <option>中等</option>
                  <option>長毛</option>
                </select>
              </div>

              <div>
                <label class="pc-label">性情／備註</label>
                <select class="pc-select" v-model="modalPet.temper">
                  <option value="" disabled>請選擇</option>
                  <option>溫和</option>
                  <option>敏感</option>
                  <option>容易緊張</option>
                </select>
              </div>

              <div>
                <label class="pc-label">毛孩年齡</label>
                <div class="pc-number-with-suffix">
                  <input class="pc-input" type="number" min="0" v-model.number="modalPet.age" placeholder="歲" />
                  <span>歲</span>
                </div>
              </div>

              <div>
                <label class="pc-label">體重</label>
                <div class="pc-number-with-suffix">
                  <input class="pc-input" type="number" step="0.1" min="0" v-model.number="modalPet.weight"
                    placeholder="kg" />
                  <span>kg</span>
                </div>
              </div>

              <div>
                <label class="pc-label">已結紮</label>
                <div class="pc-radio-inline">
                  <label><input class="pc-radio" type="radio" value="是" v-model="modalPet.neuter" />
                    是</label>
                  <label><input class="pc-radio" type="radio" value="否" v-model="modalPet.neuter" />
                    否</label>
                  <label><input class="pc-radio" type="radio" value="不確定" v-model="modalPet.neuter" />
                    不確定</label>
                </div>
              </div>

              <div>
                <label class="pc-label">已植晶片</label>
                <div class="pc-radio-inline">
                  <label><input class="pc-radio" type="radio" value="是" v-model="modalPet.chip" />
                    是</label>
                  <label><input class="pc-radio" type="radio" value="否" v-model="modalPet.chip" />
                    否</label>
                  <label><input class="pc-radio" type="radio" value="不確定" v-model="modalPet.chip" />
                    不確定</label>
                </div>
              </div>

              <div class="md:col-span-2">
                <label class="pc-label">備註</label>
                <textarea class="pc-textarea" v-model="modalPet.remark" placeholder="請輸入毛孩是否需要特別協助等情況" />
              </div>
            </div>
          </div>

          <!-- 底部操作列 -->
          <div class="pc-modal-footer">
            <button class="btn-ghost" type="button" @click="closeModal">
              取消
            </button>
            <button class="btn-primary" type="button" @click="savePet">
              確認
            </button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped src="../../../styles/pages/Customers/Booking/grooming.css"></style>