<template>
  <div id="app">

    <!-- App Navbar -->
    <app-nav-bar></app-nav-bar>

    <sidebar ref="sidebar"
      @toggled="handleExpand">

      <!-- slot for sidebar content -->
      <sidebar-menu v-if="menuActive"></sidebar-menu>

      <keep-alive>

        <brewery-info
                v-if="identifyActive"
                :feature="selectedBrewery">
        </brewery-info>

      </keep-alive>

    </sidebar>

    <map-view
            ref="mapView"
            @toggle-identify="identifyActivePanel"
            @cleared-selection="clearSelection"
            @brewery-identified="showBreweryInfo"
            @toggle-menu="menuActivePanel">
    </map-view>

    <b-modal id="login-modal" :hide-footer="true">
      <login-page @sign-up="signUp"></login-page>
    </b-modal>

  </div>
</template>

<script>
  import MapView from './components/MapViewMglv';
  import AppNavBar from './components/AppNavBar';
  import Sidebar from './components/Sidebar';
  import BreweryInfo from './components/BreweryInfo';
  import SidebarMenu from './components/SidebarMenu';
  import LoginPage from './components/LoginPage';

  export default {
    name: 'app',
    components: {
      AppNavBar,
      MapView,
      Sidebar,
      SidebarMenu,
      BreweryInfo,
      LoginPage
    },

    data(){
      return {
        selectedBrewery: null,
        menuActive: true,
        identifyActive: false
      }
    },
    mounted(){hook.app = this;},

    methods: {

      signUp(){
        console.log('clicked signup')
      },

      showBreweryInfo(brewery){
        // force panel to open with identify active
        this.selectedBrewery = brewery;
        if (brewery){
          this.$refs.sidebar.expand();
          this.menuActive = false;
          this.identifyActive = true;
        }
      },

      clearSelection(){
        this.selectedBrewery = null;
        if (this.identifyActive){
          this.$refs.sidebar.collapse();
        }
      },

      menuActivePanel(){
        // if identify is shown, toggle on menu
        if (this.identifyActive && this.$refs.sidebar.active){
          this.identifyActive = false;
          this.menuActive = true;
        } else {
          this.identifyActive = false;
          this.menuActive = true;
          this.$refs.sidebar.toggle();
        }

      },

      identifyActivePanel(){
        if (this.menuActive && this.$refs.sidebar.active){
          this.menuActive = false;
          this.identifyActive = true;
        } else {
          this.menuActive = false;
          this.identifyActive = true;
          this.$refs.sidebar.toggle();
        }
      },

      handleExpand(expanded){
        // console.log('sidebar toggled: ', expanded);
        // listen for sidebar to open and update move map's left position
        document.querySelector('#map').style.left = `${expanded ? 350: 0}px`;
        if (!expanded){
          this.clearActiveButtons();
        } else {
          this.activateButton(`.expand-${this.menuActive ? 'menu': 'identify'}`)
        }

      },

      clearActiveButtons(){
        const active = document.querySelectorAll('.control-btn-active');
        active.forEach(e => e.className = e.className.replace(/\bcontrol-btn-active\b/g, ""));
      },

      activateButton(selector){
        this.clearActiveButtons();
        const btn = document.querySelector(selector);
        if (this.$refs.sidebar.active){
          if (btn.className.indexOf('control-btn-active') < 0){
            btn.className += ' control-btn-active';
          } else {
            btn.className.replace('control-btn-active', '');
          }
        }
      }
    },

    watch: {
      menuActive(newVal){
        // handle state when panel is already open, and switched from identify to menu
        if (newVal){
          this.activateButton('.expand-menu');
        }
      },

      identifyActive(newVal){
        // handle state when panel is already open, and switched from menu to identify
        if (newVal){
          this.activateButton('.expand-identify');
        }
      },

    }
  }
</script>

<style>

  .control-btn-active {
    background-color: orange;
  }

  .control-btn-active > button {
    color: white !important;
  }

  #app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
    /*margin-top: 60px;*/
  }

</style>
