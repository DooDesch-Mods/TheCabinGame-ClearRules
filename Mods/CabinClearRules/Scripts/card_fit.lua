local M={}
local function size(value,label)
    assert(type(value)=="number" and value==value and value>0 and value<math.huge,label.." must be finite and positive")
    return value
end
function M.capture(record)
    record.original_size=size(record.widget.Description_Line1.Font.Size,"original description font size")
end
local function font_size(record,wanted)
    local text=record.widget.Description_Line1
    if text.Font.Size==wanted then return end
    -- The native TextBlock remains the font provider; only its size changes.
    local font=text.Font
    font.Size=wanted
    text:SetFont(font)
    assert(text.Font.Size==wanted,"description font size readback differs")
    record.widget:InvalidateLayoutAndVolatility()
    record.widget:ForceLayoutPrepass()
end
function M.restore(record)
    font_size(record,record.original_size)
    record.fit_done=false
end
function M.update(record,enabled,log)
    if not enabled then
        font_size(record,record.original_size)
        record.fit_done=true
        return
    end
    if record.fit_done then return end
    local text=record.widget.Description_Line1
    local parent=text:GetParent()
    assert(parent and parent:IsValid() and parent:GetClass():GetFullName()=="Class /Script/UMG.VerticalBox","native description VerticalBox unavailable")
    local slot=parent.Slot
    assert(slot and slot:IsValid() and slot:GetClass():GetFullName()=="Class /Script/UMG.CanvasPanelSlot","native card CanvasPanelSlot unavailable")
    local anchors,offsets=slot:GetAnchors(),slot:GetOffsets()
    assert(anchors.Minimum.X==0 and anchors.Minimum.Y==0 and anchors.Maximum.X==1 and anchors.Maximum.Y==1,"original card full-canvas anchors differ")
    -- Original card WidgetComponents render512x512; world-widget cached geometry stays zero.
    local width=512-offsets.Left-offsets.Right
    local height=512-offsets.Top-offsets.Bottom
    size(width,"native card canvas width");size(height,"native card canvas height")
    local padding=text.Slot.Padding
    local available_width=width-padding.Left-padding.Right
    size(available_width,"native description width")
    record.widget:ForceLayoutPrepass()
    local desired=text:GetDesiredSize()
    local total=parent:GetDesiredSize()
    assert(type(desired.X)=="number" and type(desired.Y)=="number" and desired.X==desired.X and desired.Y==desired.Y,"native description desired size readback invalid")
    assert(type(total.Y)=="number" and total.Y==total.Y and total.Y<math.huge,"native card desired height readback invalid")
    if desired.Y<=0 or total.Y<=0 then
        if not record.geometry_pending then log("info","description layout pending: "..record.title);record.geometry_pending=true end
        return
    end
    if record.geometry_pending then log("info","description layout available: "..record.title);record.geometry_pending=false end
    local available_height=height-(total.Y-desired.Y)
    size(available_height,"native description height")
    if desired.X<=available_width+0.5 and total.Y<=height+0.5 then
        record.fit_done=true
        log("info","description fits: "..record.title.."; font="..text.Font.Size.."; desired="..desired.X.."x"..desired.Y.."; available="..available_width.."x"..available_height)
        return
    end
    local current=size(text.Font.Size,"current description font size")
    local smaller=math.ceil(current)-1
    assert(smaller>0,"description cannot fit native card bounds: "..record.title.."; desired="..desired.X.."x"..desired.Y.."; available="..available_width.."x"..available_height)
    font_size(record,smaller)
end
return M
