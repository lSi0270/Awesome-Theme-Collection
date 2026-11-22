/**
 * Optional Awesome Theme Collection naming feature.
 * Adapted from the idea and algorithms in tcrgit/ha-no-device-prefix (MIT).
 * See THIRD_PARTY_NOTICES.md. This affects browser display data only.
 */
(() => {
  if (window.__atcHaNamingInstalled) return;
  window.__atcHaNamingInstalled = true;
  const keep = new Set(['keepprefix', 'keepdeviceprefix']);
  const omit = new Set(['omitprefix', 'omitdeviceprefix', 'noprefix', 'nodeviceprefix']);
  const normalize = value => String(value).toLowerCase().replace(/[^a-z0-9]/g, '');
  let settings = {enabled: false, opt_in_mode: true}; // fail closed
  let main = null;

  function strip(text, prefixes) {
    if (!text) return text;
    for (const prefix of prefixes) {
      if (prefix && text.startsWith(prefix) && text.length > prefix.length) {
        const rest = text.slice(prefix.length).replace(/^[\s\-:_]+/, '').trim();
        if (rest) return rest.charAt(0).toUpperCase() + rest.slice(1);
      }
    }
    return text;
  }

  function cleaned(hass) {
    if (!settings.enabled || !hass?.states || !hass?.entities || !hass?.devices) return hass;
    const entities = {...hass.entities};
    const states = {...hass.states};
    let changed = false;
    for (const [id, meta] of Object.entries(hass.entities)) {
      if (!meta?.device_id || !states[id]) continue;
      const device = hass.devices[meta.device_id];
      if (!device) continue;
      const labels = (device.labels || []).map(normalize);
      if (labels.some(x => keep.has(x))) continue;
      const forceOmit = labels.some(x => omit.has(x));
      if (settings.opt_in_mode && !forceOmit) continue;
      const names = [device.name_by_user, device.name].filter(Boolean);
      if (!names.length) continue;
      const state = states[id];
      const friendly = state.attributes?.friendly_name || '';
      const metaName = meta.name || meta.original_name;
      if (!forceOmit && !metaName && names.includes(friendly)) continue;
      const newFriendly = strip(friendly, names);
      if (newFriendly !== friendly && state.attributes) {
        states[id] = {...state, attributes: {...state.attributes, friendly_name: newFriendly}};
        changed = true;
      }
      const newMetaName = metaName ? strip(metaName, names) : metaName;
      if (newMetaName !== metaName || meta.next_name_part === 'device') {
        entities[id] = {...meta, name: newMetaName, original_name: newMetaName, next_name_part: undefined};
        changed = true;
      }
    }
    return changed ? {...hass, entities, states} : hass;
  }

  async function refresh() {
    try {
      const response = await fetch('/awesome_theme_collection/ha-naming-settings.json', {cache: 'no-store'});
      if (!response.ok) return;
      const data = await response.json();
      const updated = {enabled: data.enabled === true, opt_in_mode: data.opt_in_mode !== false};
      const changed = settings.enabled !== updated.enabled || settings.opt_in_mode !== updated.opt_in_mode;
      settings = updated;
      if (changed && main?.hass) main.requestUpdate('hass');
    } catch (err) {
      console.debug('[ATC HA-Namensgebung] Einstellungen nicht verfügbar', err);
    }
  }

  function attach() {
    main = document.querySelector('home-assistant');
    if (!main) {setTimeout(attach, 200); return;}
    let prototype = main;
    let descriptor;
    while (prototype && !descriptor) {
      descriptor = Object.getOwnPropertyDescriptor(prototype, 'hass');
      prototype = Object.getPrototypeOf(prototype);
    }
    if (!descriptor?.set || !descriptor?.get) {setTimeout(attach, 200); return;}
    const original = descriptor;
    Object.defineProperty(main, 'hass', {
      configurable: true,
      get() {return original.get.call(this);},
      set(value) {
        try {original.set.call(this, cleaned(value));}
        catch (err) {console.warn('[ATC HA-Namensgebung] Anzeigeanpassung fehlgeschlagen', err); original.set.call(this, value);}
      },
    });
    refresh();
    setInterval(refresh, 30000);
  }
  attach();
})();
