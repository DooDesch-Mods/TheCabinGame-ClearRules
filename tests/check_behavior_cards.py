from pathlib import Path
from lupa.lua54 import LuaRuntime

ROOT=Path(__file__).resolve().parents[1]
vm=LuaRuntime(unpack_returned_tuples=True)
path=ROOT/'Mods/CabinClearRules/Scripts/main.lua'
vm.globals().main_source=path.read_text(encoding='utf-8')
vm.globals().main_path=path.as_posix()
vm.execute('''
function FText(value) return {ToString=function() return value end} end
function FindAllOf() return {} end
mod={store={values={enabled=true}},hooks={},observers={},logs={}}
function mod:bind(path,callback) self.hooks[path]=callback end
function mod:observe(name,callback) self.observers[name]=callback end
function mod:log(level,message) self.logs[#self.logs+1]={level,message} end
package.preload.cabin_runtime=function() return {start=function() return mod end,valid=function(v) return v and v:IsValid() end} end
library={};function library:IsValid() return true end
function library:GetLocalSize(geometry) return {X=geometry.X,Y=geometry.Y} end
function StaticFindObject(path) assert(path=="/Script/UMG.Default__SlateBlueprintLibrary");return library end
assert(load(main_source,"@"..main_path))()
function make_widget(address,font_size,width,height)
    local font_object={original_font=true}
    local text={value="original",Font={Size=font_size,FontObject=font_object,TypefaceFontName="Default",OutlineSettings={size=1}},width=width,height=height,font_calls=0}
    function text:IsValid() return true end
    function text:SetText(value) self.value=value:ToString() end
    function text:GetText() return FText(self.value) end
    function text:SetFont(value) assert(value.FontObject==font_object and value.TypefaceFontName=="Default" and value.OutlineSettings.size==1);self.Font=value;self.font_calls=self.font_calls+1 end
    function text:GetCachedGeometry() return {X=self.width,Y=self.height} end
    function text:GetDesiredSize()
        if self.width<=0 or self.height<=0 then return {X=0,Y=0} end
        local glyph=self.Font.Size*0.55
        local columns=math.max(1,math.floor(math.max(1,self.width)/glyph))
        local lines,max_width=0,0
        for line in (self.value:gsub("\\r\\n","\\n").."\\n"):gmatch("(.-)\\n") do
            lines=lines+math.max(1,math.ceil(#line/columns));max_width=math.max(max_width,math.min(#line,columns)*glyph)
        end
        return {X=max_width,Y=lines*self.Font.Size*1.25}
    end
    local canvas_slot={};function canvas_slot:IsValid() return true end
    function canvas_slot:GetClass() return {GetFullName=function() return "Class /Script/UMG.CanvasPanelSlot" end} end
    function canvas_slot:GetAnchors() return {Minimum={X=0,Y=0},Maximum={X=1,Y=1}} end
    function canvas_slot:GetOffsets()
        local width=text.width>0 and text.width+24 or 472
        local height=text.height>0 and text.height+214 or 496
        return {Left=(512-width)/2,Right=(512-width)/2,Top=(512-height)/2,Bottom=(512-height)/2}
    end
    local parent={Slot=canvas_slot};function parent:IsValid() return true end
    function parent:GetClass() return {GetFullName=function() return "Class /Script/UMG.VerticalBox" end} end
    function parent:GetDesiredSize()
        local desired=text:GetDesiredSize();return {X=desired.X+24,Y=desired.Y>0 and desired.Y+214 or 0}
    end
    function text:GetParent() return parent end
    text.Slot={Padding={Left=12,Right=12,Top=0,Bottom=0}}
    function text:GetCachedGeometry() return {X=0,Y=0} end
    local widget={Description_Line1=text,title_original=true,footer_original=true}
    function widget:IsValid() return true end
    function widget:GetAddress() return address end
    function widget:InvalidateLayoutAndVolatility() end
    function widget:ForceLayoutPrepass() end
    return widget
end
function fill(widget,title,original)
    local route=title=="The Thief" and "ChanceCard_W" or title=="The Visitor" and "VisitorCard_W" or "Card_W"
    local callback=assert(mod.hooks["/Game/CabinGameContent/BoardGameStuff/Cards/CardComponents/"..route.."."..route.."_C:SetInfo_E"])
    callback({get=function() return widget end},{get=function() return FText(title) end},{get=function() return FText(original) end})
end
function settle() for _=1,32 do mod.observers["card descriptions"]() end end
local rules=require("rules")
local count=0
for title,rule in pairs(rules) do
    count=count+1
    local original=("original flavour preserved. "):rep(12).."\\r\\n\\r\\noriginal ending."
    local original_size=title=="The Visitor" and 22 or 20
    local widget=make_widget(count,original_size,420,210)
    fill(widget,title,original);settle()
    local text=widget.Description_Line1;local desired=text:GetDesiredSize()
    assert(text.value==original.."\\n\\n"..rule and desired.X<=420.5 and desired.Y<=210.5)
    assert(text.Font.Size<original_size and widget.title_original and widget.footer_original)
    local calls=text.font_calls;settle();assert(text.font_calls==calls)
    mod.store.values.enabled=false;settle();assert(text.value==original and text.Font.Size==original_size)
    mod.store.values.enabled=true;settle();assert(text.value==original.."\\n\\n"..rule and text.Font.Size<original_size)
    text.value="another card";fill(widget,"Unknown card","another card");settle()
    assert(text.value=="another card" and text.Font.Size==original_size)
end
assert(count==7)
local pending=make_widget(100,20,0,0)
fill(pending,"The Knight","original");local calls=pending.Description_Line1.font_calls
settle();assert(pending.Description_Line1.Font.Size==20 and pending.Description_Line1.font_calls==calls)
local waits=0;for _,entry in ipairs(mod.logs) do if entry[2]=="description layout pending: The Knight" then waits=waits+1 end end
assert(waits==1)
pending.Description_Line1.width=440;pending.Description_Line1.height=240;settle()
assert(pending.Description_Line1:GetDesiredSize().Y<=240.5)
fill(pending,"The Knight","short original");settle()
mod.store.values.enabled=false;settle();assert(pending.Description_Line1.Font.Size==20)
mod.store.values.enabled=true
local small=make_widget(200,20,2,1)
fill(small,"The Knight","too small")
local ok,cause=pcall(settle)
assert(not ok and tostring(cause):find("cannot fit native card bounds",1,true))
''')
print('info: seven rule layouts, font preservation, enabled/disabled/reused/unknown cards, late geometry and impossible bounds checked; native glyph metrics pending')
