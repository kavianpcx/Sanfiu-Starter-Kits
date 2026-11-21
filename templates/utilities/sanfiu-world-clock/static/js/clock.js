(() => {
  const serverTime = Date.parse(document.querySelector("[data-server-utc]")?.dataset.serverUtc || new Date().toISOString());
  const clientStart = Date.now();
  const currentTime = () => new Date(serverTime + Date.now() - clientStart);
  const update = () => {
    const now = currentTime();
    document.querySelectorAll("time[data-zone]").forEach((node) => {
      node.textContent = new Intl.DateTimeFormat(undefined, {timeZone:node.dataset.zone,hour:"numeric",minute:"2-digit",second:"2-digit"}).format(now);
    });
    document.querySelectorAll("[data-date-zone]").forEach((node) => {
      node.textContent = new Intl.DateTimeFormat(undefined, {timeZone:node.dataset.dateZone,weekday:"long",month:"long",day:"numeric",year:"numeric"}).format(now);
    });
  };
  update(); setInterval(update, 1000);
  const form=document.getElementById("converter-form");
  if(form){
    const output=document.getElementById("converted-time");
    const from=document.getElementById("from-zone");
    const to=document.getElementById("to-zone");
    const input=document.getElementById("from-time");
    const localValue=(date,zone)=>{
      const parts=new Intl.DateTimeFormat("en-CA",{timeZone:zone,year:"numeric",month:"2-digit",day:"2-digit",hour:"2-digit",minute:"2-digit",hourCycle:"h23"}).formatToParts(date);
      const get=(type)=>parts.find((part)=>part.type===type)?.value||"00";
      return `${get("year")}-${get("month")}-${get("day")} ${get("hour")}:${get("minute")}`;
    };
    input.value=localValue(currentTime(),from.value).replace(" ","T");
    form.addEventListener("submit",(event)=>{
      event.preventDefault();
      const [datePart,timePart]=input.value.split("T");
      const [year,month,day]=datePart.split("-").map(Number);
      const [hour,minute]=timePart.split(":").map(Number);
      let candidate=new Date(Date.UTC(year,month-1,day,hour,minute));
      for(let i=0;i<3;i++){
        const parts=new Intl.DateTimeFormat("en-US",{timeZone:from.value,year:"numeric",month:"numeric",day:"numeric",hour:"numeric",minute:"numeric",hourCycle:"h23"}).formatToParts(candidate);
        const get=(type)=>Number(parts.find((part)=>part.type===type)?.value||0);
        const represented=Date.UTC(get("year"),get("month")-1,get("day"),get("hour"),get("minute"));
        candidate=new Date(candidate.getTime()+Date.UTC(year,month-1,day,hour,minute)-represented);
      }
      output.textContent=new Intl.DateTimeFormat(undefined,{timeZone:to.value,weekday:"short",month:"short",day:"numeric",hour:"numeric",minute:"2-digit",timeZoneName:"short"}).format(candidate);
    });
  }
})();
