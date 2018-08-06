import { EventBus } from "./EventBus";

function createElm(){

  // create container div
  const container = document.createElement('div');
  container.className = 'mapboxgl-ctrl mapboxgl-ctrl-group expand-menu';

  // create button
  const button = document.createElement('button');
  button.className = 'mapboxgl-ctrl-icon';
  button.onclick = function(){
    EventBus.$emit('toggle-menu');
  };

  // create icon
  const icon = document.createElement('i');
  icon.className = 'fas fa-bars';

  // return div
  button.appendChild(icon);
  container.appendChild(button);
  return container;
}

export class MenuButtonControl {
  // mapboxgl.IControl must implement these methods!
  onAdd(map){
    this._map = map;
    this._container = createElm();
    return this._container;
  }

  onRemove() {
    this._container.parentNode.removeChild(this._container);
    this._map = undefined;
  }
}