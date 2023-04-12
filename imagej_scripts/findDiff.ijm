//setTool("rectangle");

makeRectangle(0, 0, 128, 127);
run("Crop");
stackName = getTitle;
stackName
run("Slice Keeper", "first=1 last=1 increment=1");
firstSlice = getTitle
imageCalculator("Subtract create 32-bit stack", stackName,firstSlice);
//selectWindow(stackName);
setSlice(1)
run("Delete Slice");
run("Enhance Contrast", "saturated=0.35");
selectWindow(firstSlice);
close();