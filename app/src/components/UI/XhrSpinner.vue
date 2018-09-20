<template>
  <div class="xhr-spinner-container">
    <spinner :visible="state === 'working'" :text="workingText"/>

    <b-alert :show="successAlertTime" @dismissed="$emit('success-dismissed');reset()" v-if="state === 'complete'" variant="success">{{ successText }}</b-alert>
    <b-alert :show="errorAlertTime" @dismissed="$emit('error-dismissed');reset()" v-if="state === 'error'" variant="danger">{{ errorText }}</b-alert>

  </div>
</template>

<script>
  export default {
    name: "xhr-spinner",
    props: {
      options: {
        type: Object,
        default(){
          return {
            errorAlertTime: 1,
            successAlertTime: 1,
            workingText: 'Prcessing Request...',
            successText: 'Successfully Completed Operation',
            errorText: 'An Error Occurred, please try again',
          }
        }
      }
    },
    data() {
      return {
        state: 'ready'
      }
    },
    methods: {
      handleErrorDismiss(){
        this.$emit('error-dismissed');
      },
      start(){
        this.state = 'working';
      },

      stop(){
        this.state = 'complete';
      },

      error(){
        this.state = 'error';
      },

      reset(){
        this.state = 'ready';
        this.$emit('xhr-spinner-ready');
      }
    }
  }
</script>