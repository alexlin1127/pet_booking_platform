<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  disabled:   { type: Boolean, default: false },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v)
  },
  onLabel:    { type: String, default: '' },
  offLabel:   { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue', 'change'])

const isOn = computed(() => props.modelValue)
const w = computed(() => (props.size === 'lg' ? 'w-16' : props.size === 'sm' ? 'w-10' : 'w-12'))
const h = computed(() => (props.size === 'lg' ? 'h-9'  : props.size === 'sm' ? 'h-5'  : 'h-6'))
const dot = computed(() => (props.size === 'lg' ? 'h-7 w-7' : props.size === 'sm' ? 'h-4 w-4' : 'h-5 w-5'))

function toggle() {
  if (props.disabled) return
  const v = !props.modelValue
  emit('update:modelValue', v)
  emit('change', v)
}
</script>

<template>
  <button
    type="button"
    class="svc-switch"
    :class="[w, h, { 'is-on': isOn, 'is-off': !isOn, 'is-disabled': disabled }]"
    role="switch"
    :aria-checked="isOn"
    :disabled="disabled"
    @click="toggle"
  >
    <span class="svc-switch__dot" :class="dot"></span>
  </button>
  <span class="ml-2 text-sm text-gray-700 select-none">{{ isOn ? onLabel : offLabel }}</span>
</template>
    