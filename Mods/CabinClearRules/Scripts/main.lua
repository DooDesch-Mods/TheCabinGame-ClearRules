local directory = assert(debug.getinfo(1,"S").source:match("^@(.+[/\\])"))
package.path = directory .. "?.lua;" .. package.path
local runtime = require("cabin_runtime")
local mod = runtime.start(directory,require("definition"))
local rules = require("rules")
local fit = require("card_fit")
local records = {}
local function update(record)
    if not runtime.valid(record.widget) or not runtime.valid(record.widget.Description_Line1) then return false end
    local wanted = mod.store.values.enabled and (record.original .. "\n\n" .. record.rule) or record.original
    if record.rendered ~= wanted then
        record.widget.Description_Line1:SetText(FText(wanted))
        assert(record.widget.Description_Line1:GetText():ToString()==wanted,"card text readback differs")
        record.rendered = wanted
        record.fit_done = false
    end
    fit.update(record,mod.store.values.enabled,function(level,message) mod:log(level,message) end)
    return true
end
local function filled(context,title,description)
    local widget = context:get()
    if not runtime.valid(widget) then return end
    local previous=records[widget:GetAddress()]
    if previous and runtime.valid(widget.Description_Line1) then fit.restore(previous) end
    records[widget:GetAddress()] = nil
    local name = title:get():ToString()
    local rule = rules[name]
    if not rule then return end
    local record = {widget=widget,original=description:get():ToString(),rule=rule,title=name}
    fit.capture(record)
    records[widget:GetAddress()] = record
    update(record)
end
mod:bind("/Game/CabinGameContent/BoardGameStuff/Cards/CardComponents/Card_W.Card_W_C:SetInfo_E",filled)
mod:bind("/Game/CabinGameContent/BoardGameStuff/Cards/CardComponents/ChanceCard_W.ChanceCard_W_C:SetInfo_E",filled)
mod:bind("/Game/CabinGameContent/BoardGameStuff/Cards/CardComponents/VisitorCard_W.VisitorCard_W_C:SetInfo_E",filled)
mod:observe("card descriptions",function()
    for _,widget in ipairs(FindAllOf("VisitorCard_W_C") or {}) do
        if runtime.valid(widget) and runtime.valid(widget.Title) and runtime.valid(widget.Description_Line1) and not records[widget:GetAddress()] then
            local rule=rules[widget.Title:GetText():ToString()]
            if rule then
                local record={widget=widget,original=widget.Description_Line1:GetText():ToString(),rule=rule,title=widget.Title:GetText():ToString()}
                fit.capture(record)
                records[widget:GetAddress()]=record
            end
        end
    end
    for address,record in pairs(records) do if not update(record) then records[address]=nil end end
end)
return mod
