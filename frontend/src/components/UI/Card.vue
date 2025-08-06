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
    <!-- Icon 區域（有內容才渲染） -->
    <div v-if="$slots.icon" class="card-icon">
      <slot name="icon"></slot>
    </div>
    
    <!-- Caption 區域（有內容才渲染） -->
    <div v-if="$slots.caption" class="card-caption">
      <slot name="caption"></slot>
    </div>
    
    <!-- Title 區域（有內容才渲染） -->
    <div v-if="$slots.title" class="card-title">
      <slot name="title"></slot>
    </div>
    
    <!-- 內容區域（有內容才渲染） -->
    <div v-if="$slots.content" class="card-content">
      <slot name="content"></slot>
    </div>
    
    <!-- Anno 區域（有內容才渲染） -->
    <div v-if="$slots.anno" class="card-anno">
      <slot name="anno"></slot>
    </div>
    
    <!-- Title2 區域（有內容才渲染） -->
    <div v-if="$slots.title2" class="card-title2">
      <slot name="title2"></slot>
    </div>
    
    <!-- Content2 區域（有內容才渲染） -->
    <div v-if="$slots.content2" class="card-content2">
      <slot name="content2"></slot>
    </div>
    
    <!-- Count 區域（有內容才渲染） -->
    <div v-if="$slots.count" class="card-count">
      <slot name="count"></slot>
    </div>
    
    <!-- 按鈕區域 -->
    <div v-if="hasButton && $slots.button" class="card-button">
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
    @click="clickable ? handleCardClick : null"
  >
    <!-- 左側圖片區域（有內容才渲染） -->
    <div v-if="$slots.image" class="card-image">
      <slot name="image"></slot>
    </div>
    
    <!-- 右側內容區域 -->
    <div class="card-info">
      <!-- Title（有內容才渲染） -->
      <div v-if="$slots.title" class="card-title">
        <slot name="title"></slot>
      </div>
      
      <!-- 內容（有內容才渲染） -->
      <div v-if="$slots.content" class="card-content">
        <slot name="content"></slot>
      </div>
    </div>
    
    <!-- 右側按鈕區域 -->
    <div v-if="hasButton && $slots.button" class="card-button">
      <slot name="button"></slot>
    </div>
  </div>
</template>

<style></style>
