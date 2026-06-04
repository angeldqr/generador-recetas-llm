<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue: string
    label: string
    name?: string
    type?: string
    placeholder?: string
    autocomplete?: string
    inputmode?: 'none' | 'text' | 'decimal' | 'numeric' | 'tel' | 'search' | 'email' | 'url'
  }>(),
  {
    name: undefined,
    type: 'text',
    placeholder: '',
    autocomplete: undefined,
    inputmode: undefined,
  },
)

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>

<template>
  <label class="base-input">
    <span>{{ label }}</span>
    <input
      :autocomplete="autocomplete"
      :inputmode="inputmode"
      :name="name"
      :placeholder="placeholder"
      :type="type"
      :value="props.modelValue"
      @input="emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />
  </label>
</template>

<style scoped>
.base-input {
  display: grid;
  gap: 8px;
  color: var(--color-ink);
  font-family: "DM Sans", system-ui;
  font-size: 0.88rem;
  font-weight: 700;
  letter-spacing: 0;
}

.base-input input {
  width: 100%;
  min-height: 50px;
  border: 1px solid rgb(15 36 24 / 0.1);
  border-radius: 16px;
  padding: 0 16px;
  color: var(--color-ink);
  background: var(--color-soft);
  font-family: "DM Sans", system-ui;
  font-size: 0.96rem;
  outline: none;
  transition:
    background 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.base-input input:focus {
  border-color: var(--color-accent);
  background: var(--color-panel);
  box-shadow: 0 0 0 4px rgb(38 116 81 / 0.16);
}

.base-input input::placeholder {
  color: var(--color-muted);
  font-weight: 500;
}
</style>
