/* Educational boundary state adapter. AXIOMS v2.4; not a hardware safety device. */
(function (root) {
  'use strict';
  const order = ['PERMIT', 'BOUNDARY_WARNING', 'HANDOFF_REQUIRED', 'IRREVERSIBLE_TRANSITION', 'RUPTURE_BOUNDARY'];
  function ratio(delta, tau) {
    if (!Number.isFinite(delta) || !Number.isFinite(tau) || delta < 0 || tau < 0) return {R:null, state:'CONFESSION'};
    if (tau === 0) return {R:null, state:'OUT_OF_DESCRIPTION_DOMAIN'};
    const R=delta/tau;
    return Number.isFinite(R) ? {R,state:null} : {R:null,state:'CONFESSION'};
  }
  class Tracker {
    constructor(warn, handoff, irrev) {
      if (![warn,handoff,irrev].every(Number.isFinite) || !(0<=warn && warn<handoff && handoff<irrev && irrev<1)) throw Error('Invalid demo thresholds');
      this.thresholds={warn,handoff,irrev};this.targets=new Map();this.trials=[];this.trial=1;
    }
    observe(key,delta,tau,step=0) {
      const v=ratio(delta,tau), old=this.targets.get(key)||{key,irreversible:false,ruptured:false};
      if(v.state){old.inputState=v.state;old.current={delta,tau,R:null,step};this.targets.set(key,old);return {...old,state:v.state,R:null};}
      old.inputState=null;old.current={delta,tau,R:v.R,step};
      // Capture first arrival independently from the latest valid observation.
      if(v.R>=this.thresholds.irrev&&!old.irreversible){old.irreversible=true;old.irreversibleRecord={key,delta,tau,R:v.R,step,trial:this.trial};}
      if(v.R>=1&&!old.ruptured){old.ruptured=true;old.ruptureRecord={key,delta,tau,R:v.R,step,trial:this.trial};}
      old.state=old.ruptured?'RUPTURE_BOUNDARY':old.irreversible?'IRREVERSIBLE_TRANSITION':v.R>=this.thresholds.handoff?'HANDOFF_REQUIRED':v.R>=this.thresholds.warn?'BOUNDARY_WARNING':'PERMIT';
      old.latestValid={...old.current};this.targets.set(key,old);return {...old,R:v.R};
    }
    summary() {
      const items=[...this.targets.values()];
      const invalid=items.find(x=>x.inputState);
      const state=!items.length?'CONFESSION':invalid?.inputState || items.reduce((a,x)=>order.indexOf(x.state)>order.indexOf(a)?x.state:a,'PERMIT');
      return {state,trial:this.trial,thresholds:this.thresholds,targets:items,testimony:items.some(x=>x.ruptured)?'POST_RUPTURE_FIXED':'CONTINUOUS',autonomousAllowed:state==='PERMIT'||state==='BOUNDARY_WARNING'};
    }
    newTrial() {this.trials.push(this.summary());this.targets=new Map();this.trial++;}
  }
  function paint(tracker, auxStop=false, badgeIds=[], overallIds=[]) {
    const summary=tracker.summary();
    const el=document.getElementById('demo-boundary-state');
    if(el) el.textContent=JSON.stringify({...summary,auxiliaryStop:!!auxStop,previousTrials:tracker.trials},null,2);
    badgeIds.forEach((id,i)=>{const el=document.getElementById(id),v=tracker.targets.get('factor'+i);if(el&&v){el.textContent=v.inputState||v.state;el.style.color=v.inputState||v.state!=='PERMIT'?'#ffb85a':'#66ddaa';}});
    overallIds.forEach(id=>{const el=document.getElementById(id);if(el)el.textContent=summary.state+(auxStop?' / AUX_STOP':'');});
    return summary;
  }
  root.NRADemoBoundary={ratio,Tracker,paint,order};
  if(typeof module!=='undefined')module.exports=root.NRADemoBoundary;
})(typeof globalThis==='undefined'?window:globalThis);
