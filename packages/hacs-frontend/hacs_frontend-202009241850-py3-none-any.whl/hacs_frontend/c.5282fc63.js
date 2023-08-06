import{_ as i,H as s,p as t,h as a,g as e,Y as o,a1 as r,a2 as l,c as n}from"./c.01a10b33.js";import"./c.4a2021cb.js";import"./c.1ddaa9a1.js";let c=i([n("hacs-removed-dialog")],(function(i,s){return{F:class extends s{constructor(...s){super(...s),i(this)}},d:[{kind:"field",decorators:[t({attribute:!1})],key:"repository",value:void 0},{kind:"field",decorators:[t({type:Boolean})],key:"_updating",value:()=>!1},{kind:"method",key:"render",value:function(){if(!this.active)return a``;const i=this.hacs.removed.find(i=>i.repository===this.repository.full_name);return a`
      <hacs-dialog
        .active=${this.active}
        .hass=${this.hass}
        .title=${this.hacs.localize("entry.messages.removed").replace("'{repository}'","")}
      >
        <div class="content">
          <div><b>${this.hacs.localize("dialog_removed.name")}:</b> ${this.repository.name}</div>
          ${i.removal_type?a` <div>
                <b>${this.hacs.localize("dialog_removed.type")}:</b> ${i.removal_type}
              </div>`:""}
          ${i.reason?a` <div>
                <b>${this.hacs.localize("dialog_removed.reason")}:</b> ${i.reason}
              </div>`:""}
          ${i.link?a`          <div>
            </b><hacs-link .url=${i.link}>${this.hacs.localize("dialog_removed.link")}</hacs-link>
          </div>`:""}
        </div>
        <mwc-button class="uninstall" slot="primaryaction" @click=${this._uninstallRepository}
          >${this._updating?a`<ha-circular-progress active></ha-circular-progress>`:this.hacs.localize("common.uninstall")}</mwc-button
        >
        <!--<mwc-button slot="secondaryaction" @click=${this._ignoreMessage}
          >${this.hacs.localize("common.ignore")}</mwc-button
        >-->
      </hacs-dialog>
    `}},{kind:"get",static:!0,key:"styles",value:function(){return e`
      .uninstall {
        --mdc-theme-primary: var(--hcv-color-error);
      }
    `}},{kind:"method",key:"_lovelaceUrl",value:function(){var i,s;return`/hacsfiles/${null===(i=this.repository)||void 0===i?void 0:i.full_name.split("/")[1]}/${null===(s=this.repository)||void 0===s?void 0:s.file_name}`}},{kind:"method",key:"_uninstallRepository",value:async function(){if(this._updating=!0,"plugin"===this.repository.category&&this.hacs.status&&"yaml"!==this.hacs.status.lovelace_mode){(await o(this.hass)).filter(i=>i.url===this._lovelaceUrl()).forEach(i=>{r(this.hass,String(i.id))})}await l(this.hass,this.repository.id),this._updating=!1,this.active=!1}},{kind:"method",key:"_ignoreMessage",value:async function(){this._updating=!1,this.active=!1}}]}}),s);export{c as HacsRemovedDialog};
