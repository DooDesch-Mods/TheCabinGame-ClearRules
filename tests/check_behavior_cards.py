from pathlib import Path
from lupa.lua54 import LuaRuntime
ROOT=Path(__file__).resolve().parents[1]
cardVM=LuaRuntime(unpack_returned_tuples=True)
cardPath=ROOT/'Mods/CabinClearRules/Scripts/main.lua'
cardVM.globals().main_source=cardPath.read_text(encoding='utf-8')
cardVM.globals().main_path=cardPath.as_posix()
cardVM.execute('''
    function FText(value) return {ToString=function() return value end} end
    function FindAllOf() return {} end
    mod={store={values={enabled=true}},hooks={},observers={}}
    function mod:bind(path,callback) self.hooks[path]=callback end
    function mod:observe(name,callback) self.observers[name]=callback end
    package.preload.cabin_runtime=function() return {start=function() return mod end,valid=function(v) return v and v:IsValid() end} end
    assert(load(main_source,"@"..main_path))()
    text={value="original"};function text:IsValid() return true end
    function text:SetText(value) self.value=value:ToString() end;function text:GetText() return FText(self.value) end
    widget={Description_Line1=text};function widget:IsValid() return true end;function widget:GetAddress() return 42 end
    context={get=function() return widget end}
    local callback=mod.hooks["/Game/CabinGameContent/BoardGameStuff/Cards/CardComponents/Card_W.Card_W_C:SetInfo_E"]
    callback(context,{get=function() return FText("The Knight") end},{get=function() return FText("original") end})
    assert(text.value:find("Rotate the statue",1,true))
    mod.store.values.enabled=false;mod.observers["card descriptions"]();assert(text.value=="original")
    mod.store.values.enabled=true;text.value="another card"
    callback(context,{get=function() return FText("Unknown card") end},{get=function() return FText("another card") end})
    mod.observers["card descriptions"]();assert(text.value=="another card")
''')
