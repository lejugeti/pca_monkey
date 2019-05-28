data = load('C:\Users\jonny\Desktop\CA6b\April-5\data\rr014\prefront\R14001_001.mat');

knl = exp( - ( 1.6*(-2500:2:2500)/2500).^2);

%% Plot Raster Plot
trials = size(data.result(:,2));
trials = trials(1,1);
spikes = zeros(trials, 8000);
f1 = zeros(trials,1);
f2 = zeros(trials,2);
d = zeros(trials,1);


%for j = 1:6
    
    
    for i = 2:trials
        
    f1(i) = data.result{i, 4};
    f2(i) = data.result{i, 5};
    
    d(i) = sign(f1(i)-f2(i)) * (2*data.result{i, 3}-1);
        
        spike_times = 5000 + data.result{i,6}{1} - data.result{i,9};
        spikes(i, round(spike_times)) = 1;    
    end

%     %RasterPlot
%     t = (0:1:120000)-5000;
%     figure(j)
%     [x, y] = find(spikes>0);
%     plot(t(y), x, 'k.');
%end

%Sort spike trins into groups according to trial type
f1un = unique(f1);
Nf1 = length(f1un);
spike_sort = cell(length(f1un),2); %Cell array for each group
for k = 1:length(f1un)
    spike_sort{k,1} = spikes( f1 == f1un(k) & d == -1, :);
    spike_sort{k,2} = spikes( f1 == f1un(k) & d == 1, :);
end

%Compute psth
psth = zeros(Nf1*2, trials); %Array for PSTH
for k = 1:Nf1
    for j = 1:2
        avrate = mean ( spike_sort{k,j}, 1 );
        psth((j - 1)*Nf1+k,:) = conv(avrate, knl,'same');
    end
end

psth = psth * 1000; %Conversion to Hz

%Plot psth
mp = colormap;
mp = mp(round(linspace(1,64,Nf1)), : );
figure(1); clf; hold on;
for k = 1:NFf1
    plot(t, psth(k,:), 'Color', mp(k,:));
    plot(t, psth(Nf1+k,:), '--', 'Color', mp(k,:));
end


        
        
% Attempt 2
% for i = 2:trials
%     
%     spikes_unordered = data.result(i,6);
%     spikes_unordered = spikes_unordered{1,:};
%     spikes_unordered_2 = [];
%     
%     for j = 1:6
%         electrode = spikes_unordered{1,j};
%         spikes_unordered_2 = [spikes_unordered_2, electrode];
%     end
%     
%     for i = 2:trials
%         spike_times = 5000 + data.result{i:6}{elec} - data.result{i,9};
%         spikes = round(trials, round(spike_times)) = 1;    
%     
%     end
%     
%     
%     spikes(i,round(spikes_unordered)) = 1;
%     
% end



%Attempt 1
% for i = 2:trials
%     spikes_unordered_cell = {};
%     spikes_unordered_vec = [];
%     spikes_unordered_cell = data.result(i,6);
%     for j = 1:6
%         spikes_unordered_vec = spikes_unordered_vec + spikes_unordered_cell{1,j};
%     end
%     spikes(i,1) = sort(spikes_unordered_vec);
% end