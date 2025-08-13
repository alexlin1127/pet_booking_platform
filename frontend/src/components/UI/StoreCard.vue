<!-- components/UI/StoreCard.vue -->
<script setup>
const props = defineProps({
  store: { type: Object, required: true },
  variant: { type: String, default: 'default' },
  showActions: { type: Boolean, default: true },
})
const emit = defineEmits(['more', 'reserve'])

const fallback =
  'https://images.unsplash.com/photo-1601758228041-f3b2795255f1?q=80&w=1000&auto=format&fit=crop'
</script>

<template>
  <article class="store-card" :class="`store-card--${variant}`">
    <img :src="store.image || fallback" :alt="store.storeName" class="store-card__img" />

    <div class="store-card__body">
      <h3 class="store-card__title">{{ store.storeName }}</h3>

      <div class="store-card__meta">
        <div class="store-card__row">📍 {{ store.address }}</div>
        <div class="store-card__row">📞 {{ store.phone }}</div>
        <div class="store-card__row">🏷️ {{ store.services }}</div>
      </div>

      <div class="store-card__tags">
        <span v-if="store.hasGrooming" class="store-badge">美容</span>
        <span v-if="store.hasLodging" class="store-badge">住宿</span>
        <span class="store-badge" :class="store.pickup?'is-on':''">接送</span>
        <span class="store-badge" :class="store.storestatus==='營業中'?'on':'off'">
          {{ store.storestatus }}
        </span>
      </div>

      <div v-if="showActions" class="store-card__actions">
        <slot name="actions">
          <button class="btn btn-ghost" @click="emit('more', store)">了解更多</button>
          <button class="btn btn-primary" @click="emit('reserve', store)">立即預約</button>
        </slot>
      </div>
    </div>
  </article>
</template>
