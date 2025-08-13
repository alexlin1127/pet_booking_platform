<script setup>
defineProps({
  type: {
    type: String,
    default: 'vertical', // 'vertical' or 'horizontal'
    validator: (value) => ['vertical', 'horizontal'].includes(value)
  },
  clickable: {
    type: Boolean,
    default: true
  },
  hasButton: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const handleCardClick = (event) => {
  // 如果點擊的是按鈕區域，則不觸發卡片點擊事件
  if (event.target.closest('.card-button')) {
    return
  }
  emit('click', event)
}
</script>

<template>
  <!-- 直向卡片 -->
  <div 
    v-if="type === 'vertical'"
    class="vertical-card"
    :class="{ 
      'clickable': clickable && !hasButton,
      'has-button': hasButton
    }"
    @click="(clickable && !hasButton) ? handleCardClick : null"
  >
    <!-- Icon 區域 -->
    <div class="card-icon">
      <slot name="icon"></slot>
    </div>
    
    <!-- Caption 區域 -->
    <div class="card-caption">
      <slot name="caption"></slot>
    </div>
    
    <!-- Title 區域 -->
    <div class="card-title">
      <slot name="title"></slot>
    </div>
    
    <!-- 內容區域 -->
    <div class="card-content">
      <slot name="content"></slot>
      <slot name="count"></slot>
    </div>
    
    <!-- 按鈕區域 -->
    <div v-if="hasButton" class="card-button">
      <slot name="button"></slot>
    </div>
  </div>

  <!-- 橫向卡片 -->
  <div 
    v-else
    class="horizontal-card"
    :class="{ 
      'clickable': clickable,
      'has-button': hasButton
    }"
    @click="clickable&& !hasButton && handleCardClick($event)"
  >
    <!-- 左側圖片區域 -->
    <div class="card-image">
      <slot name="image"></slot>
    </div>
    
    <!-- 右側內容區域 -->
    <div class="card-info">
      <!-- Title -->
      <div class="card-title">
        <slot name="title"></slot>
      </div>
      
      <!-- 內容 -->
      <div class="card-content">
        <slot name="content"></slot>
      </div>
    </div>
    
    <!-- 右側按鈕區域 -->
    <div v-if="hasButton" class="card-button">
      <slot name="button"></slot>
    </div>
  </div>
</template>

<style></style>
