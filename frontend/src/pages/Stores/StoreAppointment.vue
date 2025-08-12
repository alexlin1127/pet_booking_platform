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
            </div></template
          >
        </div>
      </div>
    </div>
  </section>
</template>
