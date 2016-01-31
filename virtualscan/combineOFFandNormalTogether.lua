if #arg < 3 then
  print("lua command.lua model.off model.normal combined")
  return
end

normalFile = arg[1]
offFile = arg[2]
combinedFile = arg[3]

normals = {}
points = {}

-- lines = io.lines('/orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.normal')
lines = io.lines(normalFile)
k = 1
for v in lines do
  -- print(v)
  normals[k] = v
  k = k + 1  
end

-- lines = io.lines('/orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.off')
lines = io.lines(offFile)
k = -1
for v in lines do
  -- print(v)
  points[k] = v
  k = k + 1
end

-- fout = io.open('/orions4-zfs/projects/haosu/codebase/geometryprocessing/models/virtualscan/model.pointandnormal', 'w')
fout = io.open(combinedFile, 'w')
for k=1,#normals do
  tokens = {}
  for w in string.gmatch(points[k], '%S+') do table.insert(tokens, w) end  
  fout:write(tokens[1]..' '..tokens[2]..' '..tokens[3]..' '..normals[k]..'\n')  
end
fout:close()

