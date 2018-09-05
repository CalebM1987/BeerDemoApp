<template>
  <div class="home-page">
    <sidebar ref="sidebar"
             @toggled="handleExpand">

      <!-- slot for sidebar content -->
      <sidebar-menu v-if="menuActive"></sidebar-menu>

      <keep-alive>

        <!-- BREWERY IDENTIFY CONTENT -->
        <brewery-info
                v-if="identifyActive"
                :userIsAuthenticated="userIsAuthenticated"
                :feature="selectedBrewery">
        </brewery-info>

      </keep-alive>

    </sidebar>

    <!-- MAP VIEW-->
    <map-view
            ref="mapView"
            @toggle-identify="identifyActivePanel"
            @cleared-selection="clearSelection"
            @brewery-identified="showBreweryInfo"
            @toggle-menu="menuActivePanel">
    </map-view>
  </div>
</template>

<script>
  import MapView from './MapViewMglv';
  import Sidebar from './Sidebar';
  import BreweryInfo from './BreweryInfo';
  import SidebarMenu from './SidebarMenu';

  export default {
    name: "home",
    components: {
      MapView,
      Sidebar,
      SidebarMenu,
      BreweryInfo
    },

    props: {
      userIsAuthenticated: false,
    },

    data(){
      return {
        selectedBrewery: null,
        menuActive: true,
        identifyActive: false,
        sidebarActive: false,
        // userIsAuthenticated: false,
        //
      }
    },
    mounted(){hook.home = this;},

    methods: {

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
        this.sidebarActive = this.$refs.sidebar.active;
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
        this.sidebarActive = this.$refs.sidebar.active;
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

<style scoped>

</style>