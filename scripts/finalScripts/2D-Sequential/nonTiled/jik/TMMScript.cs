# read program and store the internal representation in variable prog
prog = ReadAlphabets("../../TMM.ab");
 
# store string (corresponding to system name) to variable system
system = "TMM";
 
# store output directory name to variable outDir
outDir = "./out";

#CheckProgram(prog);

SerializeReduction(prog, system, "R", "(i,j,k->i,j,k)");
Normalize(prog);
RenameVariable(prog, system, "_serR", "AccR");
setSpaceTimeMap(prog, system, "R", "(i,j->i,N,j)");
setSpaceTimeMap(prog, system, "AccR", "(i,j,k->j,i,k)");
setMemoryMap(prog, system, "AccR", "R", "(i,j,k -> i,j)");
setStatementOrdering(prog, system, "AccR", "R");

# generate codes
generateScheduledCode(prog, system, outDir);
generateWrapper(prog, system, outDir);
generateMakefile(prog, system, outDir);
