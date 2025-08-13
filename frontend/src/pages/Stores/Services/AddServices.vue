<script setup lang="ts">
import { computed, reactive, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
// ⛔️ 不要在這裡 import CSS，交給 <style src="..."> 載入
// import "@/styles/pages/Stores/storeservices.css";

type Mode = "add" | "edit" | "view";
type SrvType = "grooming" | "lodging";
type Pet = "dog" | "cat";

const route = useRoute();
const router = useRouter();

const mode = computed<Mode>(() => {
    const p = route.path;
    if (p.includes("/add")) return "add";
    if (p.includes("/edit")) return "edit";
    return "view";
});

const type = ref<SrvType>((route.params.type as SrvType) || "lodging");
const pet = ref<Pet>((route.params.pet as Pet) || "dog");

const lockType = computed(() => mode.value !== "add");

const isView = computed(() => mode.value === "view");
const isLodging = computed(() => type.value === "lodging");

const pageTitle = computed(() => {
    const action =
        mode.value === "add" ? "新增" : mode.value === "edit" ? "修改" : "查看";
    const petText = pet.value === "dog" ? "狗" : "貓";
    const srvText = type.value === "grooming" ? "美容" : "住宿";
    return `${action}${petText}${srvText}服務項目`;
});
const submitText = computed(() => (mode.value === "add" ? "新增" : "完成"));

const lodging = reactive({
    cleaning: "weekly",
    cleaningNote: "",
    intro: "",
    rooms: [
        {
            _key: cryptoRandom(),
            name: "",
            count: 1,
            prices: [
                {
                    _key: cryptoRandom(),
                    nights: 1,
                    nightUnit: "day",
                    amount: 0,
                    overtime: 0,
                    noOvertime: false,
                },
            ],
        },
    ],
});

function addRoom() {
    lodging.rooms.push({
        _key: cryptoRandom(),
        name: "",
        count: 1,
        prices: [
            {
                _key: cryptoRandom(),
                nights: 1,
                nightUnit: "day",
                amount: 0,
                overtime: 0,
                noOvertime: false,
            },
        ],
    });
}
function removeRoom(idx: number) {
    lodging.rooms.splice(idx, 1);
}
function incRoomCount(room: any) {
    room.count++;
}
function decRoomCount(room: any) {
    room.count = Math.max(0, (room.count || 0) - 1);
}
function addRoomPrice(room: any) {
    room.prices.push({
        _key: cryptoRandom(),
        nights: 1,
        nightUnit: "day",
        amount: 0,
        overtime: 0,
        noOvertime: false,
    });
}
function removeRoomPrice(room: any, pIdx: number) {
    room.prices.splice(pIdx, 1);
}

const grooming = reactive({
    itemName: "",
    intro: "",
    notice: "",
    rows: [
        {
            _key: cryptoRandom(),
            fur: "none",
            size: "small",
            hours: 0,
            mins: 0,
            price: 0,
        },
    ],
});
function addChargeRow() {
    grooming.rows.push({
        _key: cryptoRandom(),
        fur: "none",
        size: "small",
        hours: 0,
        mins: 0,
        price: 0,
    });
}
function removeChargeRow(idx: number) {
    grooming.rows.splice(idx, 1);
}

function cryptoRandom() {
    return Math.random().toString(36).slice(2) + Date.now().toString(36);
}
function goBack() {
    router.back();
}
function submit() {
    const payload = {
        mode: mode.value,
        type: type.value,
        pet: pet.value,
        lodging: isLodging.value ? lodging : undefined,
        grooming: !isLodging.value ? grooming : undefined,
    };
    console.log("submit payload:", payload);
    router.back();
}
</script>
<template>
    <div class="storeservices-page">
        <div class="ss-container">
            <h1 class="block-title">{{ pageTitle }}</h1>

            <!-- 基本：毛孩類別、服務項目 -->
            <section class="ss-card">
                <div class="ss-card-inner">
                    <!-- 毛孩類別 -->
                    <label class="ss-label">毛孩類別 *</label>
                    <div class="ss-radio-group">
                        <label>
                            <input class="ss-radio" type="radio" value="dog" v-model="pet" :disabled="isView" />
                            狗狗
                        </label>
                        <label>
                            <input class="ss-radio" type="radio" value="cat" v-model="pet" :disabled="isView" />
                            貓貓
                        </label>
                    </div>

                    <!-- 服務項目 -->
                    <div class="mt-4">
                        <label class="ss-label">服務項目 *</label>
                        <div class="ss-radio-group">
                            <label>
                                <input class="ss-radio" type="radio" value="grooming" v-model="type"
                                    :disabled="lockType || isView" />
                                美容
                            </label>
                            <label>
                                <input class="ss-radio" type="radio" value="lodging" v-model="type"
                                    :disabled="lockType || isView" />
                                住宿
                            </label>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Lodging：清潔與消毒 + 房型設定 + 住宿介紹 -->
            <template v-if="isLodging">
                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">清潔與消毒 *</label>
                        <div class="ss-radio-group">
                            <label>
                                <input class="ss-radio" type="radio" value="weekly" v-model="lodging.cleaning"
                                    :disabled="isView" />
                                每週清潔
                            </label>
                            <label>
                                <input class="ss-radio" type="radio" value="biweekly" v-model="lodging.cleaning"
                                    :disabled="isView" />
                                每兩週清潔
                            </label>
                            <label>
                                <input class="ss-radio" type="radio" value="halfmonth" v-model="lodging.cleaning"
                                    :disabled="isView" />
                                每半月清潔
                            </label>
                            <label class="ss-line">
                                <input class="ss-radio" type="radio" value="other" v-model="lodging.cleaning"
                                    :disabled="isView" />
                                其他
                                <input class="ss-input is-name" placeholder="請輸入內容" v-model="lodging.cleaningNote"
                                    :disabled="isView || lodging.cleaning !== 'other'" />
                            </label>
                        </div>
                    </div>
                </section>

                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">房型設定 *</label>

                        <div class="ss-dashed">
                            <div class="ss-group-title">新增房型及狗狗最大住宿數量</div>

                            <div v-for="(room, idx) in lodging.rooms" :key="room._key" class="ss-row">
                                <!-- 房型名稱 + 房間數 -->
                                <div class="ss-line">
                                    <div class="unit">房型名稱</div>
                                    <input class="ss-input is-name" placeholder="請輸入內容" v-model="room.name"
                                        :disabled="isView" />

                                    <div class="unit">房間數數量</div>
                                    <button class="ss-mini" @click="decRoomCount(room)" :disabled="isView">
                                        -
                                    </button>
                                    <input class="ss-input is-count" v-model.number="room.count" type="number" min="0"
                                        :disabled="isView" />
                                    <button class="ss-mini" @click="incRoomCount(room)" :disabled="isView">
                                        +
                                    </button>
                                    <div class="unit">間</div>
                                </div>

                                <!-- 價格設定：可新增多筆 -->
                                <div v-for="(price, pIdx) in room.prices" :key="price._key" class="mt-3">
                                    <div class="ss-line">
                                        <div class="unit unit-strong">價格設定</div>
                                        <div class="unit">住</div>
                                        <input class="ss-input is-count" type="number" min="1"
                                            v-model.number="price.nights" :disabled="isView" />
                                        <select class="ss-select is-count" v-model="price.nightUnit" :disabled="isView">
                                            <option value="day">天</option>
                                            <option value="month">月</option>
                                        </select>

                                        <div class="unit">每晚價格：</div>
                                        <input class="ss-input is-price" type="number" min="0" placeholder="金額"
                                            v-model.number="price.amount" :disabled="isView" />
                                        <div class="unit">元</div>
                                    </div>

                                    <div class="ss-line">
                                        <div class="unit unit-strong">超時收費 *</div>
                                        <div class="unit">每小時：</div>
                                        <input class="ss-input is-price" type="number" min="0" placeholder="金額"
                                            v-model.number="price.overtime" :disabled="isView || price.noOvertime" />
                                        <div class="unit">元</div>

                                        <label class="ss-line">
                                            <input class="ss-checkbox" type="checkbox" v-model="price.noOvertime"
                                                :disabled="isView" />
                                            不加收
                                        </label>
                                    </div>

                                    <button v-if="!isView" class="ss-icon-btn" title="刪除價格"
                                        @click="removeRoomPrice(room, pIdx)">
                                        ×
                                    </button>
                                </div>

                                <div class="ss-line mt-2" v-if="!isView">
                                    <button class="btn-primary" @click="addRoomPrice(room)">
                                        新增價格
                                    </button>
                                </div>

                                <button v-if="!isView" class="ss-icon-btn" style="right: -10px; top: -10px" title="刪除房型"
                                    @click="removeRoom(idx)">
                                    ×
                                </button>
                            </div>

                            <div class="ss-line" v-if="!isView">
                                <button class="btn-ghost" @click="addRoom">新增房型</button>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">住宿介紹 *</label>
                        <textarea class="ss-textarea" placeholder="請輸入住宿介紹" v-model="lodging.intro"
                            :disabled="isView"></textarea>
                    </div>
                </section>
            </template>

            <!-- Grooming：服務細項 + 收費標準 + 服務簡介 + 注意事項 -->
            <template v-else>
                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">服務細項 *</label>
                        <div class="ss-line">
                            <input class="ss-input is-name" placeholder="請輸入更新的服務 / 服務名稱" v-model="grooming.itemName"
                                :disabled="isView" />
                        </div>
                    </div>
                </section>

                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">收費標準 *</label>

                        <div class="ss-dashed">
                            <div class="ss-group-title">設定收費標準</div>

                            <div v-for="(row, idx) in grooming.rows" :key="row._key" class="ss-row">
                                <div class="ss-line">
                                    <div class="unit">請選擇寵物毛量、體型、服務時長及價格</div>

                                    <select class="ss-select is-count" v-model="row.fur" :disabled="isView">
                                        <option value="none">無毛</option>
                                        <option value="short">短毛</option>
                                        <option value="medium">中毛</option>
                                        <option value="long">長毛</option>
                                    </select>

                                    <select class="ss-select is-count" v-model="row.size" :disabled="isView">
                                        <option value="small">小型</option>
                                        <option value="medium">中型</option>
                                        <option value="large">大型</option>
                                    </select>

                                    <input class="ss-input is-count" type="number" min="0" v-model.number="row.hours"
                                        :disabled="isView" />
                                    <div class="unit">時</div>
                                    <input class="ss-input is-count" type="number" min="0" v-model.number="row.mins"
                                        :disabled="isView" />
                                    <div class="unit">分</div>

                                    <div class="unit">價格：</div>
                                    <input class="ss-input is-price" type="number" min="0" placeholder="金額"
                                        v-model.number="row.price" :disabled="isView" />
                                    <div class="unit">元</div>
                                </div>

                                <button v-if="!isView" class="ss-icon-btn" title="刪除" @click="removeChargeRow(idx)">
                                    ×
                                </button>
                            </div>

                            <div class="ss-line" v-if="!isView">
                                <button class="btn-ghost" @click="addChargeRow">新增</button>
                            </div>
                        </div>
                    </div>
                </section>

                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">服務簡介 *</label>
                        <textarea class="ss-textarea" placeholder="請輸入服務簡介" v-model="grooming.intro"
                            :disabled="isView"></textarea>
                    </div>
                </section>

                <section class="ss-card">
                    <div class="ss-card-inner">
                        <label class="ss-label">注意事項 *</label>
                        <textarea class="ss-textarea" placeholder="請輸入注意事項" v-model="grooming.notice"
                            :disabled="isView"></textarea>
                    </div>
                </section>
            </template>

            <!-- 底部按鈕 -->
            <div class="btn-area">
                <button class="btn-ghost" @click="goBack">
                    {{ isView ? "返回" : "取消" }}
                </button>
                <button class="btn-primary" v-if="!isView" @click="submit">
                    {{ submitText }}
                </button>
            </div>
        </div>
    </div>
</template>
